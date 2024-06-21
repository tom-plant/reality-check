# controllers.py

import random
import os
import logging
import json
import requests
from flask import session, redirect, url_for, current_app
from backend.ai_calls import get_chatgpt_response, get_dalle2_response
from backend.prompts_assembly import generate_prompts
from backend.db_operations import *

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
        'news_article': None,
        'news_photo': None,
        'instagram': None,
        'youtube': None,
        'youtube_thumbnail': None,
        'shortform': None,
        'shortform_image': None
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

    # Extract text from selected_actor and selected_strategies
    actor_text = selected_actor['text'] 
    strategy_texts = [strategy['text'] for strategy in selected_strategies] 

    current_app.logger.debug("Trying to generate prompts.")
    first_narrative = None

    for i, strategy_text in enumerate(strategy_texts):
        current_app.logger.debug(f"Processing strategy '{strategy_text}' at index {i}")
        prompt_type = 'user_followup' if i > 0 else 'both'
        
        dynamic_inserts = {
            'actor': actor_text,
            'strategy': strategy_text,
            'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id']),
        }
        
        if i > 0 and first_narrative:
            dynamic_inserts['first_narrative'] = first_narrative  # Add the first narrative as a dynamic insert

        prompts_narrative = generate_prompts(
            category='narrative',
            prompt_type=prompt_type,
            dynamic_inserts=dynamic_inserts
        )
        
        current_app.logger.debug(f"Trying to generate chatgptresponses with prompts {prompts_narrative}")

        # Handle prompt type to decide which key to use for API call
        prompt_key = 'user_followup' if i > 0 else 'user'
        narrative_response = get_chatgpt_response({
            'system': prompts_narrative.get('system', ''),
            'user': prompts_narrative.get(prompt_key, '')
        })

        chatgpt_responses[strategy_text] = narrative_response

        if i == 0:
            first_narrative = narrative_response  # Store the first narrative for later use

    current_app.logger.debug("Trying to commit session data.")
    actor_id = get_actor_id_by_actor_name(selected_actor['text'])
    session['user_data']['actor_id'] = actor_id
    session.modified = True

    return chatgpt_responses

def select_news_article_controller(narrative, strategy):
    content_batch = {}
    
    # Generate news article
    prompts_news_article = generate_prompts(
        category='news_article',
        prompt_type='both',
        dynamic_inserts={
            'narrative': narrative,
            'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id'])
        })

    news_response = get_chatgpt_response(prompts_news_article)
    if "error" in news_response:
        return news_response, 500

    content_batch['news_article'] = handle_chatgpt_output(news_response)

    headline = content_batch['news_article']['headline']

    # Intermediate call to generate image description
    prompts_image_description = generate_prompts(
        category='image_description',
        prompt_type='both',
        dynamic_inserts={
            'headline': headline
        })

    image_description_response = get_chatgpt_response(prompts_image_description)
    if "error" in image_description_response:
        return image_description_response, 500

    # Generate news photo
    prompts_news_photo = generate_prompts(
        category='news_photo',
        prompt_type='system',
        dynamic_inserts={
            'image_description': image_description_response
        })

    news_photo_response = get_dalle2_response(prompts_news_photo)
    if "error" in news_photo_response:
        return news_photo_response, 500

    content_batch['news_photo'] = news_photo_response

    # Save to session
    session['user_data']['news_article'] = content_batch['news_article']
    session['user_data']['news_photo'] = content_batch['news_photo']
    session.modified = True

    current_app.logger.debug(f"Content batch from article: {content_batch}")
    return content_batch


def select_instagram_controller(narrative, strategy):
    content_batch = {}

    # Generate instagram content
    prompts_instagram = generate_prompts(
        category='instagram',
        prompt_type='both',
        dynamic_inserts={
            'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
            'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id']),
        })

    instagram_response = get_chatgpt_response(prompts_instagram)
    if "error" in instagram_response:
        return instagram_response, 500

    content_batch['instagram'] = handle_chatgpt_output(instagram_response)

    # Save to session
    session['user_data']['instagram'] = content_batch['instagram']
    session.modified = True

    current_app.logger.debug(f"Content batch from insta: {content_batch}")
    return content_batch


def select_youtube_controller(narrative, strategy):
    content_batch = {}

    # Generate youtube content
    prompts_youtube = generate_prompts(
        category='youtube',
        prompt_type='both',
        dynamic_inserts={
            'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
            'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id']),
        })

    youtube_response = get_chatgpt_response(prompts_youtube)
    if "error" in youtube_response:
        return youtube_response, 500

    content_batch['youtube'] = handle_chatgpt_output(youtube_response)

    video_title = content_batch['youtube']

    # Intermediate call to generate image description
    prompts_thumbnail_description = generate_prompts(
        category='thumbnail_description',
        prompt_type='both',
        dynamic_inserts={
            'video_title': video_title
        })

    thumbnail_description_response = get_chatgpt_response(prompts_thumbnail_description)
    if "error" in thumbnail_description_response:
        return thumbnail_description_response, 500

    # Generate YouTube Thumbnail
    prompts_youtube_thumbnail = generate_prompts(
        category='yt_thumbnail',
        prompt_type='system',
        dynamic_inserts={
            'thumbnail_description': thumbnail_description_response
        })

    youtube_thumbnail_response = get_dalle2_response(str(prompts_youtube_thumbnail))
    if "error" in youtube_thumbnail_response:
        return youtube_thumbnail_response, 500

    content_batch['youtube_thumbnail'] = youtube_thumbnail_response

    # Save to session
    session['user_data']['youtube'] = content_batch['youtube']
    session['user_data']['youtube_thumbnail'] = content_batch['youtube_thumbnail']
    session.modified = True

    current_app.logger.debug(f"Content batch from youtube: {content_batch}")
    return content_batch


def select_shortform_controller(narrative, strategy):
    content_batch = {}

    # Generate shortform content
    prompts_shortform = generate_prompts(
        category='shortform',
        prompt_type='both',
        dynamic_inserts={
            'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
            'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id']),
        })

    shortform_response = get_chatgpt_response(prompts_shortform)
    if "error" in shortform_response:
        return shortform_response, 500

    content_batch['shortform'] = handle_chatgpt_output(shortform_response)

    # Intermediate call to generate shortform description
    prompts_shortform_description = generate_prompts(
        category='shortform_image_description',
        prompt_type='both',
        dynamic_inserts={
            'shortform_text': shortform_response
        })

    shortform_image_description_response = get_chatgpt_response(prompts_shortform_description)
    if "error" in shortform_image_description_response:
        return shortform_image_description_response, 500

    # Generate shortform image
    prompts_shortform_image = generate_prompts(
        category='shortform_image',
        prompt_type='system',
        dynamic_inserts={
            'shortform_image_description': shortform_image_description_response
        })

    shortform_image_response = get_dalle2_response(str(prompts_shortform_image))
    if "error" in shortform_image_response:
        return shortform_image_response, 500

    content_batch['shortform_image'] = shortform_image_response

     # Save to session
    session['user_data']['shortform'] = content_batch['shortform']
    session['user_data']['shortform_image'] = content_batch['shortform_image']
    session.modified = True

    current_app.logger.debug(f"Content batch from shortform: {content_batch}")
    return content_batch

def commit_primary_narrative_controller(selected_narrative, strategy):
    user_data = session['user_data']

    # Store the strategy in session for later use
    strategy_id = get_strategy_id_by_strategy_name(strategy)
    session['user_data']['strat_id'] = strategy_id
    session.modified = True

    # Combine all content batches
    combined_content_batch = {
        'news_article': user_data.get('news_article'),
        'news_photo': user_data.get('news_photo'),
        'instagram': user_data.get('instagram'),
        'youtube': user_data.get('youtube'),
        'youtube_thumbnail': user_data.get('youtube_thumbnail'),
        'shortform': user_data.get('shortform'),
        'shortform_image': user_data.get('shortform_image')
    }

    # Commit Primary Narrative to Database
    primary_narrative = create_primary_narrative(
        fact_combination_id=user_data['fact_combination_id'],
        narrative_text=selected_narrative,  
        user_id=user_data['user_id'],
        actor_id=user_data['actor_id'], 
        strat_id=strategy_id,
        news=combined_content_batch,
        _session=None
    )
    
    db.session.add(primary_narrative)
    db.session.commit()

    session['user_data']['primary_narrative_id'] = primary_narrative.id
    session.modified = True

def handle_chatgpt_output(chatgpt_response):
    # Check if the response is a string that looks like a JSON
    try:
        # Try parsing it assuming it's a JSON string
        parsed_response = json.loads(chatgpt_response)
        if isinstance(parsed_response, dict):  # Ensure it's a dictionary
            current_app.logger.debug(f"Parsed response as JSON: {parsed_response}")
            return parsed_response
        else:
            raise ValueError("Parsed JSON is not a dictionary")
    except (json.JSONDecodeError, ValueError) as e:
        # If parsing fails or it's not a dictionary, log and use the string directly
        current_app.logger.debug(f"Handling response as plain text due to: {e}")
        return {'text': chatgpt_response}

def safe_json_dumps(data):
    try:
        return json.dumps(data)
    except TypeError as e:
        current_app.logger.error(f"Failed to serialize to JSON: {e}")
        # Handle non-serializable data gracefully, perhaps by converting to string or providing a default
        return json.dumps({k: str(v) for k, v in data.items()})

def introduce_event_controller(event_details):
    # Verify user authentication
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    user_data = session['user_data']
    primary_narrative_id = user_data.get('primary_narrative_id')
    event_id = event_details.get('id')
    current_app.logger.debug(f"got user data and primary narrative and event id: {user_data} and {primary_narrative_id} and {event_id}")


    # Check for necessary data
    if not primary_narrative_id or not event_id:
        current_app.logger.debug("Missing data.")
        return {"error": "Missing data"}, 400
    
    # 2. Check if narrative-event pair already exists
    current_app.logger.debug("Check if narrative-event pair already exists.")
    narrative_event = NarrativeEvent.query.filter_by(
        narrative_id=primary_narrative_id, event_id=event_id
    ).first()

    # If it exists, return the existing event outcome text
    current_app.logger.debug("If it exists, return the existing event outcome text")
    if narrative_event:
        current_app.logger.debug("Narrative event pair found, returning existing event outcome text.")
        return {"event_outcome_text": narrative_event.event_outcome_text}

    # If it doesn't exist, generate the event outcome text using the ChatGPT call
    primary_narrative = get_primary_narrative_by_id(primary_narrative_id)
    if not primary_narrative:
        current_app.logger.debug("Narrative not found")
        return {"error": "Narrative not found"}, 404

    current_app.logger.debug("generating")
    prompts_event_outcomes = generate_prompts(
        category='event_outcome',
        prompt_type='both',
        dynamic_inserts={
            'event': event_details.get('text', ''),
            'narrative': primary_narrative.narrative_text,
        })

    event_outcome_text = get_chatgpt_response(prompts_event_outcomes)

    # Create the narrative event entry in the database
    current_app.logger.debug("add to dataset")
    narrative_event = NarrativeEvent(
        narrative_id=primary_narrative_id,
        event_id=event_id,
        event_outcome_text=event_outcome_text
    )
    db.session.add(narrative_event)
    db.session.commit()
    session['user_data']['narrative_events_id'] = narrative_event.id
    session.modified = True

    current_app.logger.debug(f"final is {event_outcome_text}")
    return {"event_outcome_text": event_outcome_text}

def identify_weaknesses_controller(updated_fact_combination, selected_strategies):    
    # Check if user is logged in
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401
    current_app.logger.debug(f"What we're wokring with is udpaedfactcombo: {updated_fact_combination} and selected_strategies {selected_strategies}")

    updated_fact_combination_id = handle_fact_combination(updated_fact_combination)
    session['user_data']['updated_fact_combination_id'] = updated_fact_combination_id
    session.modified = True

    prompts_counter_narrative = {}
    chatgpt_responses = {}

    strategy_texts = [strategy['text'] for strategy in selected_strategies] 
    current_app.logger.debug("Trying to generate prompts.")

    for i, strategy_text in enumerate(strategy_texts):
        current_app.logger.debug(f"Processing strategy '{strategy_text}' at index {i}")
        prompt_type = 'user_followup' if i > 0 else 'both'
        prompts_counter_narrative = generate_prompts(
            category='counter_narrative',
            prompt_type=prompt_type,
            dynamic_inserts={
                'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
                'updated_facts': updated_fact_combination,
                'counter_strategy': strategy_text
            })
        current_app.logger.debug(f"Trying to generate chatgptresponses with prompts {prompts_counter_narrative}")

        # Handle prompt type to decide which key to use for API call
        prompt_key = 'user_followup' if i > 0 else 'user'
        chatgpt_responses[strategy_text] = get_chatgpt_response({
            'system': prompts_counter_narrative.get('system', ''),
            'user': prompts_counter_narrative.get(prompt_key, '')
        })
    current_app.logger.debug(f"chatgpt responess for counters: {chatgpt_responses}")

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
    current_app.logger.debug(f"EFFECTIVENESS **** * ** *  ** * *  *** * * is: {effectiveness}")
    current_app.logger.debug(f"COUnterSTRATEGY text **** * ** *  ** * *  *** * * is: {strategy}")
    current_app.logger.debug(f"COUNTERSTRATEGY ID **** * ** *  ** * *  *** * * is: {counter_strategy_id}")
    current_app.logger.debug(f"STRATEGY ID **** * ** *  ** * *  *** * * is: {strategy_id}")


    prompts_election_outcomes = generate_prompts(
        category='election_outcome',
        prompt_type='both',
        dynamic_inserts={
            'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
            'counter_narrative': counter_narrative,
            'effectiveness': effectiveness,
        })
    current_app.logger.debug(f"prompts are: {prompts_election_outcomes}")
    election_outcome = get_chatgpt_response(prompts_election_outcomes)
    current_app.logger.debug(f"election_outcome is: {election_outcome}")

    # Save to Database 
    secondary_narrative = create_secondary_narrative(
        original_narrative_id=session['user_data']['primary_narrative_id'], 
        user_id=session['user_data']['user_id'],
        updated_fact_combination_id=session['user_data']['updated_fact_combination_id'], 
        narrative_text=counter_narrative, 
        counterstrat_id=session['user_data']['counterstrat_id'],
        outcome_text=election_outcome,
        news='placeholder',
        _session=None
    )
    db.session.add(secondary_narrative)
    db.session.commit()  
    session['user_data']['secondary_narrative_id'] = secondary_narrative.id
    session.modified = True

    return {"election_outcome": election_outcome, "effectiveness": effectiveness}
