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
        'user_id': 'some_user_id',
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
            system_content = get_text(language_code, 'generate_additional_narratives_system_content', selected_facts)
            user_content = get_text(language_code, 'generate_additional_narratives_user_content', selected_facts)
        else:
            # Use the different prompt for subsequent narratives, referring back to the previous one
            system_content = previous_narrative
            user_content = get_text(language_code, 'generate_additional_narratives_user_content_followup', selected_facts)

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
    # if 'user_data' not in session:
    #     return {"error": "User not logged in"}, 401     #USE THIS VERSION LATER
    if 'user_data' not in session:
        initialize_data_controller()  # Call the initialization function if 'user_data' doesn't exist
 
    # Generate News 
    # selected_facts = get_fact_combination_by_id(fact_combination_id)
    # newsjsonthing(full of headline,story,photo) = generate_news_content(selected_narrative, selected_facts):   
        # *** potentially insert another variable(?) that pulls from a file storing the chatgpt api pairings so that they're all in one place

    # Commit Primary Narrative to Database
    # fact_combination_id = user_data(fact_combination_id)
    # narrative_text = get_primary_narrative_by_id(narrative_id):
    # user_id = user_data(user_id)
    # headline = newsjsonthing(headline)
    # story = newsjsonthing(story)
    # photo_url = newsjsonthing(photo_url)
    # create_primary_narrative(fact_combination_id, narrative_text, user_id, headline, story, photo_url)

    # Store Primary Narrative ID in User Session
    session['primary_narrative_id'] = selected_narrative

    # Return a success response
    return {"message": "Narrative and facts selection processed successfully"}



def generate_news_content(selected_narrative):

    # Call the ChatGPT API
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    language_code = get_user_language_by_id(session['user_data']['user_id'])

# continue logic here





def introduce_event_controller():
    # Logic to select and send randomly selected follow-up event to the frontend
    # Check if combination of previous narrative and event exists in the database
    # If exists, retrieve news headlines and photo from the database
    # If not, call ChatGPT API to generate news headlines and DALL-E 2 API to generate photo
    
    # Placeholder for now
    return jsonify({"message": "Introduce event controller placeholder"}) #TAKE OUT JSONIFY



def identify_weaknesses_controller(new_facts, narrative):
    # Logic to send new combination of facts and narrative to ChatGPT API to update with a new narrative and story outcome
    
    # Placeholder for now
    return jsonify({"message": "Identify weaknesses controller placeholder"}) #TAKE OUT JSONIFY


