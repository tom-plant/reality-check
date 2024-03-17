# controllers.py

import random
import os
import logging
import json
import requests
from db_operations import *
from flask import session, redirect, url_for
from localization import get_text

def initialize_data_controller(user_id):
    session['user_data'] = {
        'user_id': user_id,
        'fact_combination_id': None,
        'primary_narrative_id': None, 
        'secondary_narrative_id': None,
        'narrative_events_id': None,
    }

def register_user_controller(username, email):
    # Use the create_user function to create a new user
    new_user = create_user(username=username, email=email)
    
    if new_user:
        db.session.add(new_user)
        db.session.commit()

        # Initialize data for the new user
        initialize_data_controller(new_user.id)
        
        # Store user ID in the session
        session['user_id'] = new_user.id
        
        return {"message": "User registered successfully", "user_id": new_user.id}
    else:
        return {"error": "User registration failed"}
    
def login_user_controller(username_or_email):
    # Check if user exists by username or email
    user = get_user_by_username_or_email(username_or_email)
    
    if user:
        # Store user ID in the session
        session['user_id'] = user.id
        
        return {"message": "User logged in successfully", "user_id": user.id}
    else:
        return {"error": "User not found"}


def select_facts_controller(selected_facts):

    # Ensure 'user_data' is initialized in session
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401     

    # Store the fact_combination_id in session
    print(f"Received facts: {selected_facts}")  # Log received facts
    fact_combination_id = handle_fact_combination(selected_facts)
    print(f"Fact combination ID: {fact_combination_id}")  # Log the ID of the fact combination
    session['user_data']['fact_combination_id'] = fact_combination_id

    return {"fact_combination_id": fact_combination_id} #temproary for debugging


    # # Present three narratives, generated or pulled from database
    # narratives = get_narratives_by_fact_combination(selected_facts)
    # num_narratives = len(narratives)

    # if num_narratives >= 3:
    #     random_narratives = random.sample(narratives, 3) if num_narratives > 3 else narratives
    #     return {"narratives": random_narratives}
    # else:
    #     num_additional_narratives = 3 - num_narratives
    #     additional_narratives = generate_additional_narratives(selected_facts, num_additional_narratives)
    #     combined_narratives = narratives + additional_narratives
    #     return {"narratives": combined_narratives}

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

def generate_additional_narratives(selected_facts, num_additional_narratives):

    API_KEY = os.environ.get('API_KEY')

    # Call the ChatGPT API
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    language_code = get_user_language_by_id(user_id=session['user_data']['user_id'])
    narratives = []
    previous_narrative = None


    for i in range(num_additional_narratives):
        if i == 0 or num_additional_narratives == 1:
            # Use the initial prompt for the first narrative or if only one is needed
            system_content = get_text(language_code, "chatgpt_prompts", "additional_narratives", 'generate_additional_narratives_system_content', replacements={"evidence": ', '.join(selected_facts)})
            user_content = get_text(language_code, "chatgpt_prompts", "additional_narratives", 'generate_additional_narratives_user_content', replacements={"evidence": ', '.join(selected_facts)})

        else:
            # Use the different prompt for subsequent narratives, referring back to the previous one
            system_content = previous_narrative
            user_content_followup = get_text(language_code, "chatgpt_prompts", "additional_narratives", 'generate_additional_narratives_user_content_followup', replacements={"evidence": ', '.join(selected_facts)})

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }

        response = requests.post(chatGPTUrl, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_json = response.json()
            narrative = response_json['choices'][0]['message']['content'].strip()
            narratives.append(narrative)
            previous_narrative = narrative  # Save the last generated narrative for reference in the next loop iteration
        else:
            print(f"Error in generate_additional_narratives: {response.status_code} - {response.text}")
            narratives.append(f"Error generating narrative {i+1}")
    return narratives



def select_narrative_controller(selected_narrative):
    # # Ensure 'user_data' is initialized in session
    # if 'user_data' not in session:
    #     return {"error": "User not logged in"}, 401

    # Set language code and selected facts
    language_code = get_user_language_by_id(user_id=session['user_data']['user_id'])
    selected_facts = get_fact_combination_by_id(session['user_data']['fact_combination_id'])

    # Call the function to generate news content
    news_content = generate_news_content(language_code, "primary_narrative", selected_narrative, selected_facts)

    # Commit Primary Narrative to Database
    primary_narrative = create_primary_narrative(
        fact_combination_id=session['user_data']['fact_combination_id'],
        narrative_text=selected_narrative,
        user_id=session['user_data']['user_id'],
        headline=news_content["headline"],
        story=news_content["story"],
        photo_url=news_content["image_url"],  
        _session=None
    )
    db.session.add(primary_narrative)
    db.session.commit()
    session['user_data']['primary_narrative_id'] = primary_narrative.id

    # Return the news data as a JSON response
    return {"news_content": news_content}

def generate_prompts(language_code, category, context, selected_narrative, selected_facts, headline=None):

    if isinstance(selected_facts, list):
        selected_facts = ", ".join(selected_facts)  # Join if list
    replacements = {
        "narrative": selected_narrative,
        "evidence": selected_facts
    }

    # Always generate headline prompts
    prompts = {
        "headline_system": get_text(language_code, category, context, "headline_system", replacements),
        "headline_user": get_text(language_code, category, context, "headline_user", replacements)
    }

    # Generate story and image prompts only if headline is provided
    if headline:
        # Update replacements with the generated headline
        replacements["headline"] = headline

        # Generate story prompts
        prompts["story_system"] = get_text(language_code, category, context, "story_system", replacements)
        prompts["story_user"] = get_text(language_code, category, context, "story_user", replacements)

        # Generate image prompt
        prompts["image_prompt"] = get_text(language_code, category, context, "image_prompt", replacements)

    # Generate secondary_system and secondary_user prompts for secondary_narrative context
    if context == "secondary_narrative":
        prompts["secondary_system"] = get_text(language_code, category, context, "secondary_system", replacements)
        prompts["secondary_user"] = get_text(language_code, category, context, "secondary_user", replacements)

    return prompts

def generate_news_content(language_code, context, selected_narrative, selected_facts):

    API_KEY = os.environ.get('API_KEY')

    # Function to send requests to the ChatGPT API
    def get_chatgpt_response(system_content, user_content):
        
        # ChatGPT API settings
        chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }

        try:
            response = requests.post(chatGPTUrl, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                error_message = f"Failed to generate text content. API Error: {response.status_code} - {response.text}"
                print(error_message)
            raise Exception(error_message)  # Halting the process by raising an exception
        except Exception as e:
            print(f"Network or request error occurred: {str(e)}")
            raise Exception(f"Network or request error occurred: {str(e)}")  # Re-raise to halt the process

    # Function to send requests to the DALL-E-2 API 
    def get_dalle2_response(prompt):
        
        API_KEY = os.environ.get('API_KEY')

        # DALL-E-2 API settings
        dalleUrl = 'https://api.openai.com/v1/images/generations'
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "model": "dall-e-2",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }

        try: 
            response = requests.post(dalleUrl, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                image_data = response.json()['data'][0]
                return image_data.get('url')  # Assuming the API returns the URL directly
            elif response.status_code == 400:
                error_info = response.json().get('error', {})
                if error_info.get('code') == 'content_policy_violation':
                    # Handle content policy violation specifically
                    print("Content policy violation error: ", error_info.get('message'))
                    # You might want to log this error, return a default 'safe' image, or handle it in some other way
                    return "No URL due to safety violation"  # Placeholder for your default safe image URL
                else:
                    # Handle other 400 errors
                    error_message = f"Failed to generate image. API Error: {response.status_code} - {response.text}"
                    raise Exception(error_message)
            else:
                # Handle other non-200 responses
                error_message = f"Failed to generate image. API Error: {response.status_code} - {response.text}"
                print(error_message)
                raise Exception(error_message)  

                # Check for content policy violation specifically
                if response.status_code == 400 and "content_policy_violation" in response.text:
                    raise Exception("Content policy violation detected. Adjusting the prompt may be necessary.")  
                raise Exception(error_message)
        except Exception as e:
            print(f"Network or request error occurred: {str(e)}")
            raise Exception(f"Network or request error occurred: {str(e)}")  

    # Execute Generations
    # Gnerate only headline prompts and headline
    headline_prompts = generate_prompts(language_code, "chatgpt_prompts", context, selected_narrative, selected_facts)
    headline = get_chatgpt_response(headline_prompts['headline_system'], headline_prompts['headline_user'])
    if not headline:
        raise Exception("Failed to generate headline, halting process.")

    # Generate story and image prompts using the actual headline
    full_prompts = generate_prompts(language_code, "chatgpt_prompts", context, selected_narrative, selected_facts, headline=headline)

    # Generate story using story prompts
    story = get_chatgpt_response(full_prompts['story_system'], full_prompts['story_user'])
    if not story:
        raise Exception("Failed to generate story, halting process.")

    # Generate image URL using the image prompt
    image_url = get_dalle2_response(full_prompts['image_prompt'])

    # Combine the generated content
    news_content = {
        "headline": headline,
        "story": story,
        "image_url": image_url
    }
    
    return news_content

def introduce_event_controller():
    # Check if user is logged in
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    # Randomly select an event
    Event = get_random_event()
    if not Event:
        return {"error": "No event found"}, 404
    
    # Extract necessary values from session
    language_code = get_user_language_by_id(user_id=session['user_data']['user_id'])
    context = "event_narrative"
    primary_narrative_id = session['user_data'].get('primary_narrative_id')
    event_id = Event.id
    event = [Event.text]

    # Find or create the narrative event news content and its id
    news_content, narrative_event_id = handle_narrative_event(primary_narrative_id, event_id, event, language_code, context)
    # Check if an error response was returned from handle_narrative_event
    if isinstance(news_content, dict) and 'error' in news_content:
        return news_content, narrative_event_id  # Directly return the error response
    session['user_data']['narrative_events_id'] = narrative_event_id
    
    return {"event_news_content": news_content, "narrative_event_id": narrative_event_id}, 200

def handle_narrative_event(primary_narrative_id, event_id, event, language_code, context):

    #Check if new or existing
    narrative_event_id = get_narrative_events_id_by_narrative_and_event(primary_narrative_id, event_id)

    if narrative_event_id is None:
        primary_narrative = get_primary_narrative_by_id(primary_narrative_id)
        if primary_narrative is None:
            return {"error": "Selected narrative not found"}, 404
        news_content = generate_event_news_content(primary_narrative, context, language_code, event)
        if news_content is None:
            return {"error": "Failed to handle narrative event"}, 500

        narrative_event = create_narrative_event(primary_narrative_id, event_id, news_content['headline'], news_content['story'], news_content['image_url'])
        db.session.add(narrative_event)
        db.session.commit()
        return news_content, narrative_event_id
        if news_content is None:
            return {"error": "Failed to handle narrative event"}, 500
    else:
        news_content = get_news_content_by_narrative_events_id(narrative_event_id)
        if news_content is None:
            return {"error": "Failed to handle narrative event"}, 500
        return news_content, narrative_event_id

def generate_event_news_content(primary_narrative, context, language_code, event, _session=None):
    session = _session or db.session

    try:
        # Attempt to generate news content based on the narrative and event
        event_news_content = generate_news_content(language_code, context, primary_narrative, event)
    except Exception as e:
        # Handle content generation failure
        logging.error(f"Error generating content: {e}")
        return None
    
    return event_news_content



def identify_weaknesses_controller(updated_fact_combination):     # Receive Updated Fact Combination
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
    news_content, secondary_narrative_id = handle_narrative_update(primary_narrative_id, updated_fact_combination_id, updated_fact_combination, language_code, context) 
    # Store secondary_narrative_id in user session
    session['user_data']['secondary_narrative_id'] = secondary_narrative_id

    if news_content is None:
        return {"error": "Failed to handle narrative event"}, 500
    
    return {"secondary_news_content": news_content, "secondary_narrative_id": secondary_narrative_id}, 200

def handle_narrative_update(primary_narrative_id, updated_fact_combination_id, updated_fact_combination, language_code, context, _session=None):
    session = _session or db.session

    #Check if new or existing
    secondary_narrative_id = get_secondary_narrative_id_by_fact_combination_and_primary_narrative(primary_narrative_id, updated_fact_combination_id) 

    # If secondary_narrative is new
    if secondary_narrative_id is None:
        primary_narrative = get_primary_narrative_by_id(primary_narrative_id)
        
        # Generate Secondary Narrative
        secondary_narrative_text = generate_secondary_narrative(language_code, context, primary_narrative.narrative_text, updated_fact_combination)

        # Generate News for Secondary Narrative
        news_content = generate_secondary_news_content(language_code, context, secondary_narrative_text, updated_fact_combination)

        if news_content is None:
            return None, None

        # Save to Database 
        secondary_narrative = create_secondary_narrative(
            primary_narrative_id=primary_narrative_id, 
            updated_fact_combination_id=updated_fact_combination_id, 
            narrative_text=secondary_narrative_text, 
            resulting_headline=news_content['headline'], 
            resulting_story=news_content['story'], 
            resulting_photo_url=news_content['image_url'],
            user_id=primary_narrative.user_id  # Set user_id from the primary_narrative's user_id
        )
        db.session.add(secondary_narrative)
        session.commit()  # Don't forget to commit the session

        return news_content, secondary_narrative_id
    # If not new
    else:
        news_content = get_news_content_by_secondary_narrative_id(secondary_narrative_id)
        return news_content, secondary_narrative_id

#use generate_additional_narratives as a model
def generate_secondary_narrative(language_code, context, primary_narrative, updated_fact_combination):

    API_KEY = os.environ.get('API_KEY')

    # Call the ChatGPT API
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Set Up
    secondary_narrative_prompts = generate_prompts(language_code, "chatgpt_prompts", context, primary_narrative.narrative_text, updated_fact_combination)

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
        "max_tokens": 100
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

def generate_conclusion(): 
    pass
    
    # A final function that creates some kind of final storyline that wraps up not only the narrative but also the crisis in general. 
    # This is stored in the secondary narrative table




