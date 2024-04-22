# controllers.py

import random
import os
import logging
import json
import requests
from flask import session, redirect, url_for, current_app
from ai_calls import get_chatgpt_response, get_dalle2_response
from prompts_assembly import generate_prompts, get_text
from db_operations import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initialize_data_controller(user_id):
    session['user_data'] = {
        'user_id': user_id,
        'fact_combination_id': None,
        'actor_id': None,
        'strat_id': None,
        'counterstrat_id': None,
        'updated_fact_combination_id': None,
        'primary_narrative_id': None, 
        'secondary_narrative_id': None,
        'narrative_events_id': None,
    }

def register_user_controller(username, email):
    new_user = create_user(username=username, email=email)
    if new_user:
        db.session.add(new_user)
        db.session.commit()
        initialize_data_controller(new_user.id)
        session['user_id'] = new_user.id
        return {"message": "User registered successfully", "user_id": new_user.id}
    else:
        return {"error": "User registration failed"}

def get_all_facts_controller():
    try:
        facts = get_all_facts()
        facts_list = [{'id': fact.id, 'text': fact.text, 'language': fact.language} for fact in facts]
        return {"facts": facts_list}
    except:
        return {"error": "Failed to fetch facts from the database."}, 500

def get_all_events_controller():
    try:
        events = get_all_events()  
        events_list = [{'id': event.id, 'text': event.text, 'language': event.language} for event in events]
        return {"events": events_list}
    except Exception as e:
        print(f"Database error: {str(e)}")
        return {"error": "Failed to fetch events from the database."}, 500

def get_all_actors_controller():
    try:
        actors = get_all_actors()  
        actors_list = [{'id': actor.id, 'text': actor.text, 'language': actor.language} for actor in actors]
        return {"actors": actors_list}
    except Exception as e:
        print(f"Database error: {str(e)}")
        return {"error": "Failed to fetch actors from the database."}, 500

def get_all_strats_controller():
    try:
        strats = get_all_strats()  
        strats_list = [{'id': strat.id, 'text': strat.text, 'language': strat.language} for strat in strats]
        return {"strats": strats_list}
    except Exception as e:
        print(f"Database error: {str(e)}")
        return {"error": "Failed to fetch strats from the database."}, 500

def get_all_counterstrats_controller():
    try:
        counterstrats = get_all_counterstrats()  
        counterstrats_list = [{'id': counterstrat.id, 'text': counterstrat.text, 'language': counterstrat.language} for counterstrat in counterstrats]
        return {"counterstrats": counterstrats_list}
    except Exception as e:
        print(f"Database error: {str(e)}")
        return {"error": "Failed to fetch counterstrats from the database."}, 500

def select_facts_controller(selected_facts):
    current_app.logger.debug("In the select facts controller.")

    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401     

    current_app.logger.debug("Trying to handle facts.")
    # Store the fact_combination_id in session
    fact_combination_id = handle_fact_combination(selected_facts)
    current_app.logger.debug("Trying to add to user data.")

    session['user_data']['fact_combination_id'] = fact_combination_id
    session.modified = True

    return {"message": "Fact combination added to session and database successfully"}

def handle_fact_combination(selected_facts):
    
    # Find if the combination exists
    fact_combination_id = get_fact_combination_id_by_facts(selected_facts)
    
    # If not found, create a new combination and get its ID
    if fact_combination_id is None:
        fact_combination = create_fact_combination(','.join(map(str, sorted(selected_facts))))
        db.session.add(fact_combination)
        db.session.commit()
        fact_combination_id = fact_combination.id
    
    return fact_combination_id

def build_narrative_controller(selected_actor, selected_strategies):
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401  

    current_app.logger.debug("Entered build narative controller.")
    prompts_narrative = {}
    chatgpt_responses = {}
    current_app.logger.debug("Trying to generate prompts.")
    for strategy in selected_strategies:
        prompts_narrative[strategy] = generate_prompts(
            file_path='prompts.json',
            category='narrative',
            prompt_type='both',
            dynamic_inserts={
                'actor': get_text('prompt_inserts', 'actor', selected_actor),
                'strategy': get_text('prompt_inserts', 'construction_strategy', strategy),
                'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id']),
            })
        current_app.logger.debug("Trying to generate chatgptresponses.")
        chatgpt_responses[strategy] = get_chatgpt_response(prompts_narrative[strategy])
    
    current_app.logger.debug("Trying to commit session data.")
    actor_id = get_actor_id_by_actor_name(selected_actor)
    session['user_data']['actor_id'] = actor_id
    session.modified = True

    return chatgpt_responses

def select_narrative_controller(selected_narrative, strategy):
    # Ensure 'user_data' is initialized in session
    current_app.logger.debug(f"Session Data: {session}")
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    # Store the strategy in session for later use
    strategy_id = get_strategy_id_by_strategy_name(strategy)
    session['user_data']['strat_id'] = strategy_id
    session.modified = True

    content_batch = {}

    # Generate news article
    prompts_news_article = generate_prompts(
        file_path='prompts.json',
        category='news_article',
        prompt_type='both',
        dynamic_inserts={
            'narrative': selected_narrative['text'],
            'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id'])
        })

    content_batch['news_article'] = get_chatgpt_response(prompts_news_article)
    headline = content_batch['news_article']['headline']

    # Generate news photo
    prompts_news_photo = generate_prompts(
        file_path='prompts.json',
        category='news_photo',
        prompt_type='system',
        dynamic_inserts={
            'headline': headline
        })

    content_batch['news_photo'] = get_dalle2_response(prompts_news_photo)

    # Generate social media content
    prompts_social_media_content = generate_prompts(
        file_path='prompts.json',
        category='social_media_content',
        prompt_type='both',
        dynamic_inserts={
            'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
            'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id']),
        })

    content_batch['social_media_content'] = get_chatgpt_response(prompts_social_media_content)
    video_title = content_batch['social_media_content']['youtube']

    # Generate YouTube thumbnail
    prompts_youtube_thumbnail = generate_prompts(
        file_path='prompts.json',
        category='youtube_thumbnail',
        prompt_type='system',
        dynamic_inserts={
            'video_title': video_title
        })

    content_batch['youtube_thumbnail'] = get_dalle2_response(prompts_youtube_thumbnail)

    # Commit Primary Narrative to Database
    primary_narrative = create_primary_narrative(
        fact_combination_id=session['user_data']['fact_combination_id'],
        narrative_text=selected_narrative['text'],  
        user_id=session['user_data']['user_id'],
        actor_id=session['user_data']['actor_id'], 
        strat_id=strategy_id,
        news=content_batch,
        _session=None
    )
    db.session.add(primary_narrative)
    db.session.commit()
    session['user_data']['primary_narrative_id'] = primary_narrative.id
    session.modified = True

    # Return the news data as a JSON response
    content_json = json.dumps(content_batch)
    return content_json

def introduce_event_controller(event_details):
    # Verify user authentication
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    user_data = session['user_data']
    primary_narrative_id = user_data.get('primary_narrative_id')
    event_id = event_details.get('id')

    # Check for necessary data
    if not primary_narrative_id or not event_id:
        return {"error": "Missing data"}, 400

    # 2. Check if narrative-event pair already exists
    narrative_event = NarrativeEvent.query.filter_by(
        narrative_id=primary_narrative_id, event_id=event_id
    ).first()

    # If it exists, return the existing event outcome text
    if narrative_event:
        current_app.logger.debug("Narrative event pair found, returning existing event outcome text.")
        return {"event_outcome_text": narrative_event.event_outcome_text}

    # If it doesn't exist, generate the event outcome text using the ChatGPT call
    primary_narrative = get_primary_narrative_by_id(primary_narrative_id)
    if not primary_narrative:
        return {"error": "Narrative not found"}, 404

    prompts_event_outcomes = generate_prompts(
        file_path='prompts.json',
        category='event_outcome',
        prompt_type='both',
        dynamic_inserts={
            'event': event_details.get('text', ''),
            'narrative': primary_narrative.narrative_text,
        })

    event_outcome_text = get_chatgpt_response(prompts_event_outcomes)

    # Create the narrative event entry in the database
    narrative_event = NarrativeEvent(
        narrative_id=primary_narrative_id,
        event_id=event_id,
        event_outcome_text=event_outcome_text
    )
    db.session.add(narrative_event)
    db.session.commit()
    session['user_data']['narrative_events_id'] = narrative_event.id
    session.modified = True

    return {"event_outcome_text": event_outcome_text}

def identify_weaknesses_controller(updated_fact_combination, selected_strategies):    
    # Check if user is logged in
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    updated_fact_combination_id = handle_fact_combination(updated_fact_combination)
    session['user_data']['updated_fact_combination_id'] = updated_fact_combination_id
    session.modified = True

    prompts_counter_narrative = {}
    for strategy in selected_strategies:
        prompts_counter_narrative[strategy] = generate_prompts(
            file_path='prompts.json',
            category='counter_narrative',
            prompt_type='both',
            dynamic_inserts={
                'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
                'updated_facts': updated_fact_combination,
                'strategy': get_text('prompt_inserts', 'counter_strategies', strategy)
            })

    chatgpt_responses = {}
    for strategy, prompts in prompts_counter_narrative.items():
        chatgpt_response = get_chatgpt_response(prompts)
        chatgpt_responses[strategy] = chatgpt_response

    return chatgpt_responses

def conclusion_controller(counter_narrative, strategy):
    # Check if user is logged in
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    # Store the strategy in session for later use
    strategy_id = session['user_data']['strat_id']
    counter_strategy_id = get_counter_strategy_id_by_name(strategy)
    session['user_data']['counterstrat_id'] = counter_strategy_id
    session.modified = True

    effectiveness = get_effectiveness_by_ids(strategy_id, counter_strategy_id)

    prompts_election_outcomes = generate_prompts(
        file_path='prompts.json',
        category='election_outcome',
        prompt_type='both',
        dynamic_inserts={
            'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
            'counter_narrative': counter_narrative,
            'crisis_background': get_text('plot_context', 'crisis_background'),
            'effectiveness': effectiveness,
            'outcomes': get_text('plot_context', 'outcomes')
        })

    election_outcome = get_chatgpt_response(prompts_election_outcomes)

    # Save to Database 
    secondary_narrative = create_secondary_narrative(
        original_narrative_id=session['user_data']['primary_narrative_id'], 
        updated_fact_combination_id=session['user_data']['updated_fact_combination_id'], 
        narrative_text=counter_narrative, 
        counterstrat_id=session['user_data']['counterstrat_id'],
        news=election_outcome,
        _session=None
    )
    db.session.add(secondary_narrative)
    db.session.commit()  
    session['user_data']['secondary_narrative_id'] = secondary_narrative.id
    session.modified = True

    return {"election_outcome": election_outcome}
