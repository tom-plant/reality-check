# controllers.py
import random
import json
import requests
from db_operations import *
from config import API_KEY
from flask import session
from localization import get_text


def initialize_data_controller():

    # Initialize 'user_data' in session
    session['user_data'] = {
        'fact_combination_id': None,
        'user_id': None,
        'primary_narrative_id': None,
        'secondary_narrative_id': None,
        'narrative_events_id': None,
    }



def select_facts_controller(selected_facts):

    # Ensure 'user_data' is initialized in session
    # if 'user_data' not in session:
    #     return {"error": "User not logged in"}, 401     #USE THIS VERSION LATER
    if 'user_data' not in session:
        initialize_data_controller()  # Call the initialization function if 'user_data' doesn't exist

 
    # Use the handle_fact_combination function and store the fact_combination_id in session
    fact_combination_id = handle_fact_combination(selected_facts)
    session['user_data']['fact_combination_id'] = fact_combination_id

    # The rest of your existing logic for selecting narratives
    narratives = get_narratives_by_fact_combination(selected_facts)
    num_narratives = len(narratives)

    if num_narratives >= 3:
        random_narratives = random.sample(narratives, 3) if num_narratives > 3 else narratives
        return {"narratives": random_narratives}
    else:
        num_additional_narratives = 3 - num_narratives
        additional_narratives = generate_additional_narratives(selected_facts, num_additional_narratives)
        combined_narratives = narratives + additional_narratives
        return {"narratives": combined_narratives}

def handle_fact_combination(selected_facts):

    # Find if the combination exists
    fact_combination_id = find_fact_combination_id_by_facts(selected_facts)
    
    # If not found, create a new combination and get its ID
    if fact_combination_id is None:
        fact_combination = create_fact_combination(','.join(map(str, sorted(selected_facts))))
        fact_combination_id = fact_combination.id
    
    return fact_combination_id

def generate_additional_narratives(selected_facts, num_additional_narratives):

    # Call the ChatGPT API
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    language_code = get_user_language_by_id(session['user_data']['user_id'])
    narratives = []
    previous_narrative = None


    for i in range(num_additional_narratives):
        if i == 0 or num_additional_narratives == 1:
            # Use the initial prompt for the first narrative or if only one is needed
            system_content = get_text(language_code, "chatgpt_prompts", "additional_narratives", 'generate_additional_narratives_system_content', replacements={"selected_facts": ', '.join(selected_facts)})
            user_content = get_text(language_code, "chatgpt_prompts", "additional_narratives", 'generate_additional_narratives_user_content', replacements={"selected_facts": ', '.join(selected_facts)})

        else:
            # Use the different prompt for subsequent narratives, referring back to the previous one
            system_content = previous_narrative
            user_content_followup = get_text(language_code, "chatgpt_prompts", "additional_narratives", 'generate_additional_narratives_user_content_followup', replacements={"selected_facts": ', '.join(selected_facts)})

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
    print(narratives)
    return narratives



def select_narrative_controller(selected_narrative):
    # Ensure 'user_data' is initialized in session
    if 'user_data' not in session:
        return {"error": "User not logged in"}, 401

    # Set language code and selected facts
    language_code = get_user_language_by_id(session['user_data']['user_id'])
    selected_facts = get_fact_combination_by_id(session['user_data']['fact_combination_id'])

    # Call the function to generate news content
    news_data = generate_news_content(language_code, "primary_narrative", selected_narrative, selected_facts)

    # Return the news data as a JSON response
    return {"news_data": news_data}

def generate_prompts(language_code, category, context, selected_narrative, selected_facts, headline=None):
    replacements = {
        "selected_narrative": selected_narrative,
        "selected_facts": ", ".join(selected_facts)
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

    return prompts

def generate_news_content(language_code, context, selected_narrative, selected_facts):

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
    event = get_random_event()
    if not event:
        return {"error": "No event found"}, 404

    # Extract necessary values from session
    language_code = get_user_language_by_id(session['user_data']['user_id'])
    selected_facts = get_fact_combination_by_id(session['user_data']['fact_combination_id'])
    context = "event_narrative"

    # Get selected_narrative from user data id and database search
    narrative_id = session['user_data'].get('primary_narrative_id')
    selected_narrative = get_primary_narrative_by_id(narrative_id)
    if not selected_narrative:
        return {"error": "Selected narrative not found"}, 404

    # Handle event selection but do not create a new NarrativeEvent yet
    narrative_event, is_new_event = handle_event_selection(selected_narrative, event)

    # If the NarrativeEvent is new, generate content; otherwise, fetch existing content
    if is_new_event:
        news_content = generate_event_news_content(selected_narrative, context, language_code, selected_facts, narrative_event, _session=None)
        if news_content is None:
            return {"error": "Failed to generate news content"}, 500
        return {"event_news_content": news_content}, 200
    else:
        news_content = get_news_content_by_narrative_events_id(narrative_event.id)
        return {"event_news_content": news_content}, 200

    session.commit()  # Now commit the new NarrativeEvent with its content
    # Make sure primary narrative and narrative events are linked. Think they are but check

def handle_event_selection(selected_narrative, event, _session=None):
    session = _session or db.session
    narrative_event = check_narrative_events_existence(selected_narrative.id, event.id, _session=None)
    
    if narrative_event is None:
        # Create a placeholder NarrativeEvent, but don't store news content yet
        narrative_event = NarrativeEvent(selected_narrative.id, event.id)
        session.add(narrative_event)
        session.flush()  # Flush to assign an ID to the new narrative_event, but don't commit yet
        return narrative_event, True  # Return the new event and a flag indicating it's new

    return narrative_event, False  # Return the existing event and a flag indicating it's not new

def generate_event_news_content(selected_narrative, context, language_code, selected_facts, narrative_event, _session=None):
    session = _session or db.session

    try:
        # Attempt to generate news content based on the narrative and event
        event_news_content = generate_news_content(language_code, context, selected_narrative, selected_facts)
    except Exception as e:
        # Handle content generation failure
        print(f"Error generating content: {e}")
        return None

    # Update the narrative_event with the generated content
    narrative_event.resulting_headline = event_news_content['headline']
    narrative_event.resulting_story = event_news_content['story']
    narrative_event.resulting_photo_url = event_news_content.get('photo_url')

    return event_news_content



def identify_weaknesses_controller(updated_fact_combination):     # Receive Updated Fact Combination

    # Retrieve Primary Narratives 
    primary_narrative = get_primary_narrative_by_id(session['user_data']['primary_narrative_id']) 

    # Handle event selection but do not create a new NarrativeEvent yet
    updated_narrative, is_new_narrative = handle_narrative_update(primary_narrative, updated_fact_combination)
    
    # Prep Information for News Generation
    context = "secondary_narrative"
    language_code = get_user_language_by_id(session['user_data']['user_id'])
    updated_facts = get_updated_fact_combination_by_id(session['user_data']['updated_fact_combination_id']) #NEED TO CREATE THIS CRUD OEPRATION

    # If the updated_narrative  is new, generate content; otherwise, fetch existing content. 
    if is_new_narrative:
        # Attempt to generate news content based on the narrative and event
        news_content = generate_secondary_news_content(selected_narrative, context, language_code, selected_facts, narrative_event, _session=None)
        if news_content is None:
            return {"error": "Failed to generate news content"}, 500
        return {"event_news_content": news_content}, 200
    else:
        news_content = get_news_content_by_secondary_narrative_id(secondary_narrative.id)
        return {"secondary_news_content": news_content}, 200

    session.commit()  # Now commit the new NarrativeEvent with its content

    return secondary_news_content


def handle_narrative_update(updated_narrative, updated_fact_combination, _session=None):
    session = _session or db.session
    updated_narrative = check_updated_narrative_existence(selected_narrative.id, event.id, _session=None) # CREATE NEW CRUD OPERATION
    
    if updated_narrative is None:
        # Create a placeholder UpdatedNarrative, but don't store news content yet
        updated_narrative = UpdatedNarrative(updated_narrative.id, event.id)
        session.add(updated_narrative)
        session.flush()  # Flush to assign an ID to the new narrative_event, but don't commit yet
        return updated_narrative, True  # Return the new event and a flag indicating it's new

    return updated_narrative, False  # Return the existing event and a flag indicating it's not new


def generate_secondary_news_content(updated_narrative, context, language_code, updated_facts, secondary_narrative, _session=None):
    session = _session or db.session

    try:
        # Attempt to generate news content based on the narrative and event
        updated_news_content = generate_news_content(language_code, context, selected_narrative, selected_facts)
    except Exception as e:
        # Handle content generation failure
        print(f"Error generating content: {e}")
        return None

    # Update the narrative_event with the generated content
    updated_narrative.resulting_headline = event_news_content['headline']
    updated_narrative.resulting_story = event_news_content['story']
    updated_narrative.resulting_photo_url = event_news_content.get('photo_url')

    return secondary_news_content



 # PART 4    # A final function that creates some kind of final storyline that wraps up not only the narrative but also the crisis in general. 
             # This is stored in the secondary narrative table


     # Placeholder for now
    return {"message": "Identify weaknesses controller placeholder"}


