# controllers.py

import random
import os
import logging
import json
import requests
from flask import session, redirect, url_for, current_app

if os.getenv('FLASK_ENV') == 'production':
    from backend.localization import get_text
    from backend.db_operations import *
else:
    from localization import get_text
    from db_operations import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initialize_data_controller(user_id):
    session['user_data'] = {
        'user_id': user_id,
        'fact_combination_id': None,
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

def select_facts_controller(selected_facts):
    if os.getenv('FLASK_ENV') == 'production':
        from backend.app import app
    else:
        from app import app
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401     

    # Store the fact_combination_id in session
    fact_combination_id = handle_fact_combination(selected_facts)
    session['user_data']['fact_combination_id'] = fact_combination_id
    session.modified = True

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
    if os.getenv('FLASK_ENV') == 'production':
        from backend.app import app
    else:
        from app import app
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401     





prompts = generate_prompts(
    category='narrative',
    sub_category='system',  # or 'user', depending on what you need
    crisis_background='The crisis began when...',
    actor_background='The main actors in this crisis are...'
)



def generate_prompts(category, sub_category, needs_user_prompt=True, **kwargs):
    system_prompt = get_text('prompts', sub_category, 'system', **kwargs)

    # Initialize a dictionary to hold the prompts
    prompt_data = {'system': system_prompt}

    # Check if a user prompt is needed
    if needs_user_prompt:
        user_prompt = get_text('prompts', sub_category, 'user', **kwargs)
        prompt_data['user'] = user_prompt

    return prompt_data

def get_text(main_category, sub_category, prompt_type=None, **replacements):
    # Load the prompts from the JSON file
    with open('prompts.json', 'r') as file:
        prompts = json.load(file)

    text = prompts[main_category][sub_category]
    if prompt_type:
        text = text[prompt_type]

    # Use string formatting to replace placeholders with actual content
    return text.format(**replacements)







def select_narrative_controller(selected_narrative):
    # Ensure 'user_data' is initialized in session
    current_app.logger.debug(f"Session Data: {session}")
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    # Set language code and selected facts
    selected_narrative_text = selected_narrative['text']  
    language_code = get_user_language_by_id(user_id=session['user_data']['user_id'])
    selected_facts = get_fact_combination_by_id(session['user_data']['fact_combination_id'])

    # Call the function to generate news content
    news_content = generate_news_content(language_code, "primary_narrative", selected_narrative_text, selected_facts)

    # Commit Primary Narrative to Database
    primary_narrative = create_primary_narrative(
        fact_combination_id=session['user_data']['fact_combination_id'],
        narrative_text=selected_narrative['text'],  
        user_id=session['user_data']['user_id'],
        headline=news_content["headline"],
        story=news_content["story"],
        photo_url=news_content["image_url"],  
        _session=None
    )
    db.session.add(primary_narrative)
    db.session.commit()
    session['user_data']['primary_narrative_id'] = primary_narrative.id
    session.modified = True

    # Return the news data as a JSON response
    return {"news_content": news_content}


def generate_news_content(language_code, context, selected_narrative, selected_facts):



    # Execute Generations
    # Gnerate only headline prompts and headline
    current_app.logger.debug(f"trying to call headline prompts with {language_code}, 'chatgpt_prompts', {context}, {selected_narrative}, and {selected_facts}")
    headline_prompts = generate_prompts(language_code, "chatgpt_prompts", context, selected_narrative, selected_facts)
    current_app.logger.debug(f"Calling ChatGPT API for headline with prompts {headline_prompts}")
    headline = get_chatgpt_response(headline_prompts['headline_system'], headline_prompts['headline_user'])
    if not headline:
        raise Exception("Failed to generate headline, halting process.")
    current_app.logger.debug(f"Generated Headline: {headline}")

    # Generate story and image prompts using the actual headline
    full_prompts = generate_prompts(language_code, "chatgpt_prompts", context, selected_narrative, selected_facts, headline=headline)

    # Generate story using story prompts
    story = get_chatgpt_response(full_prompts['story_system'], full_prompts['story_user'])
    if not story:
        raise Exception("Failed to generate story, halting process.")
    current_app.logger.debug(f"Generated story: {story}")

    # Generate image URL using the image prompt
    current_app.logger.debug("Calling DALL-E-2 API for image")
    image_url = get_dalle2_response(full_prompts['image_prompt'])
    current_app.logger.debug(f"Generated imageurl: {image_url}")


    # Combine the generated content
    news_content = {
        "headline": headline,
        "story": story,
        "image_url": image_url
    }
    
    return news_content

def introduce_event_controller(Event):
    # Check if user is logged in
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401
    
    # Extract necessary values from session
    language_code = get_user_language_by_id(user_id=session['user_data']['user_id'])
    context = "event_narrative"
    primary_narrative_id = session['user_data'].get('primary_narrative_id')
    event_id = Event['id'] 
    event = Event['text']

    # Find or create the narrative event news content and its id
    news_content, narrative_event_id = handle_narrative_event(primary_narrative_id, event_id, event, language_code, context)
    # Check if an error response was returned from handle_narrative_event
    if isinstance(news_content, dict) and 'error' in news_content:
        return news_content, narrative_event_id  # Directly return the error response

    session['user_data']['narrative_events_id'] = narrative_event_id
    session.modified = True
    
    current_app.logger.debug(f'final news content in controller: {news_content}')
    return {"event_news_content": news_content}

def handle_narrative_event(primary_narrative_id, event_id, event, language_code, context):

    #Check if new or existing
    narrative_event_id = get_narrative_events_id_by_narrative_and_event(primary_narrative_id, event_id)

    if narrative_event_id is None:
        current_app.logger.debug(f"Running new conditional for narrative_event")
        primary_narrative = get_primary_narrative_by_id(primary_narrative_id)
        primary_narrative_text = primary_narrative.narrative_text
        if primary_narrative is None:
            return {"error": "Selected narrative not found"}, 404
        news_content = generate_event_news_content(primary_narrative_text, context, language_code, event)
        if news_content is None:
            return {"error": "Failed to handle narrative event"}, 500

        narrative_event = create_narrative_event(primary_narrative_id, event_id, news_content['headline'], news_content['story'], news_content['image_url'])
        db.session.add(narrative_event)
        db.session.commit()
        return news_content, narrative_event_id
        if news_content is None:
            return {"error": "Failed to handle narrative event"}, 500
    else:
        current_app.logger.debug(f"Running existing conditional for narrative event")
        news_content = get_news_content_by_narrative_events_id(narrative_event_id)
        if news_content is None:
            return {"error": "Failed to handle narrative event"}, 500
        return news_content, narrative_event_id

def generate_event_news_content(primary_narrative, context, language_code, event, _session=None):
    session = _session or db.session

    try:
        # Attempt to generate news content based on the narrative and event
        event_news_content = generate_news_content(language_code, context, primary_narrative, event)
        current_app.logger.debug(f"Finished generating news content in generate_event_news_content: {event_news_content}")
    except Exception as e:
        # Handle content generation failure
        logging.error(f"Error generating content: {e}")
        return None
    
    return event_news_content



def identify_weaknesses_controller(updated_fact_combination):    
    # Check if user is logged in
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    # Extract necessary values from session for news generation
    user_id = session['user_data']['user_id']
    language_code = get_user_language_by_id(user_id=session['user_data']['user_id'])
    context = "secondary_narrative"
    primary_narrative_id = session['user_data']['primary_narrative_id']

    # Find or create the updated fact combination and its id 
    updated_fact_combination_id = handle_fact_combination(updated_fact_combination)

    # Find or create the secondary narrative news content and its id
    news_content, secondary_narrative_text = handle_narrative_update(primary_narrative_id, updated_fact_combination_id, updated_fact_combination, language_code, context) 
    # Store secondary_narrative_id in user session
    
    if news_content is None:
        return {"error": "Failed to handle narrative event"}, 500

    secondary_narrative_id = session['user_data']['secondary_narrative_id']
    # Construct secondary narrative object

    secondary_narrative = {
        "id": secondary_narrative_id,
        "text": secondary_narrative_text
    }
    
    current_app.logger.debug(f"FINAL returning secondary_narrative: {secondary_narrative} and news: {news_content}")
    return {"secondary_news_content": news_content, "secondary_narrative": secondary_narrative}

def handle_narrative_update(primary_narrative_id, updated_fact_combination_id, updated_fact_combination, language_code, context):
    current_app.logger.debug("ENTERING HANDLE NARRATIVE UPDATE")
    current_app.logger.debug(f"Session Data: {session}")
    #Check if new or existing
    secondary_narrative_id = get_secondary_narrative_id_by_fact_combination_and_primary_narrative(primary_narrative_id, updated_fact_combination_id) 

    # If secondary_narrative is new
    if secondary_narrative_id is None:
        current_app.logger.debug("ENTERING secondarynarrative new conditional")
        primary_narrative = get_primary_narrative_by_id(primary_narrative_id)
        current_app.logger.debug(f"primary_narrative= {primary_narrative}")

        primary_narrative_text = primary_narrative.narrative_text
        current_app.logger.debug(f"primary_narrative_text= {primary_narrative_text}")

        
        # Generate Secondary Narrative
        secondary_narrative_text = generate_secondary_narrative(language_code, context, primary_narrative_text, updated_fact_combination)

        # Generate News for Secondary Narrative
        news_content = generate_secondary_news_content(language_code, context, secondary_narrative_text, updated_fact_combination)

        if news_content is None:
            return None, None

        # Save to Database 
        secondary_narrative = create_secondary_narrative(
            original_narrative_id=primary_narrative_id, 
            updated_fact_combination_id=updated_fact_combination_id, 
            narrative_text=secondary_narrative_text, 
            resulting_headline=news_content['headline'], 
            resulting_story=news_content['story'], 
            resulting_photo_url=news_content['image_url'],
            user_id=primary_narrative.user_id,  # Set user_id from the primary_narrative's user_id
            _session=None
        )
        db.session.add(secondary_narrative)
        db.session.commit()  # Don't forget to commit the session
        session['user_data']['secondary_narrative_id'] = secondary_narrative.id
        session.modified = True

        return news_content, secondary_narrative_text
    # If not new
    else:
        current_app.logger.debug("ENTERING secondarynarrative old conditional")
        news_content = get_news_content_by_secondary_narrative_id(secondary_narrative_id)
        secondary_narrative_text = secondary_narrative.narrative_text
        return news_content, secondary_narrative_id, secondary_narrative_text

def generate_secondary_narrative(language_code, context, primary_narrative, updated_fact_combination):

    API_KEY = os.environ.get('API_KEY')

    # Call the ChatGPT API
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Set Up
    secondary_narrative_prompts = generate_prompts(language_code, "chatgpt_prompts", context, primary_narrative, updated_fact_combination)

    # Use the initial prompt for the first narrative or if only one is needed
    system_content = secondary_narrative_prompts['secondary_system']
    user_content = secondary_narrative_prompts['secondary_user']
       
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    # Initialize secondary_narrative to handle potential errors
    secondary_narrative = None

    response = requests.post(chatGPTUrl, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_json = response.json()
        secondary_narrative = response_json['choices'][0]['message']['content'].strip()
    else:
        print(f"Error in generate_secondary_narrative: {response.status_code} - {response.text}")
        # Handle the error appropriately, maybe set secondary_narrative to a default value or raise an exception

    # Ensure secondary_narrative has been set before returning it
    if secondary_narrative is not None:
        return secondary_narrative
    else:
        # Handle the case where secondary_narrative wasn't generated successfully
        raise Exception("Failed to generate secondary narrative")


def generate_secondary_news_content(language_code, context, secondary_narrative, updated_fact_combination): 

    try:
        # Attempt to generate news content based on the narrative and event
        secondary_news_content = generate_news_content(language_code, context, secondary_narrative, updated_fact_combination)
    except Exception as e:
        # Handle content generation failure
        logging.error(f"Error generating content: {e}")
        return None
    
    return secondary_news_content



def conclusion_controller(): 
     # Check if user is logged in
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401
    
    # Extract necessary values from session for news generation
    user_id = session['user_data']['user_id']
    language_code = get_user_language_by_id(user_id=session['user_data']['user_id'])
    context = "conclusion"
    primary_narrative_id = session['user_data']['primary_narrative_id']
    secondary_narrative_id = session['user_data']['secondary_narrative_id']
    selected_facts = ['conclusion']

    
    #db operations to fetch narratives
    primary_narrative = get_primary_narrative_by_id(primary_narrative_id)
    primary_narrative_text = primary_narrative.narrative_text

    secondary_narrative = get_secondary_narrative_by_id(secondary_narrative_id)
    secondary_narrative_text = secondary_narrative.narrative_text


    current_app.logger.debug('Trying to generate conclusion content')
    # Generate conclusion content
    conclusion_content = generate_conclusion(language_code, context, selected_facts, primary_narrative_text, secondary_narrative_text)
    
    if conclusion_content is None:
        return {"error": "Failed to handle conclusion"}, 500
    
    current_app.logger.debug(f"FINAL returning conclusion: {conclusion_content}")
    # Extract paragraphs from the conclusion_content
    paragraphs = conclusion_content.get("paragraphs", [])
    return {"conclusion_paragraphs": paragraphs}


def generate_conclusion(language_code, context, selected_facts, primary_narrative, secondary_narrative):

    API_KEY = os.environ.get('API_KEY')

    # Call the ChatGPT API
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Set Up
    system_content = get_text(language_code, "chatgpt_prompts", "conclusion", 'conclusion_system')
    current_app.logger.debug(f'system content: {system_content}')
    user_content = get_text(language_code, "chatgpt_prompts", "conclusion", 'conclusion_user', replacements={"primary_narrative": primary_narrative, "secondary_narrative": secondary_narrative})
    current_app.logger.debug(f'user content: {user_content}')

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.7,
        "max_tokens": 600
    }

    try:
        response = requests.post(chatGPTUrl, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            
            # Split the content into paragraphs based on two newline characters
            paragraphs = content.split('\n\n')

            # Return the list of paragraphs
            return {
                "paragraphs": paragraphs
            }
        else:
            error_message = f"Failed to generate text content. API Error: {response.status_code} - {response.text}"
            current_app.logger.error(error_message)
            raise Exception(error_message)  # Halting the process by raising an exception
    except Exception as e:
        current_app.logger.error(f"Network or request error occurred: {str(e)}")
        raise  # Re-raise to halt the process
