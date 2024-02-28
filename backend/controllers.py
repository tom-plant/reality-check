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
            system_content = get_text(language_code, 'generate_additional_narratives_system_content', replacements={"selected_facts": ', '.join(selected_facts)})
            user_content = get_text(language_code, 'generate_additional_narratives_user_content', replacements={"selected_facts": ', '.join(selected_facts)})
        else:
            # Use the different prompt for subsequent narratives, referring back to the previous one
            system_content = previous_narrative
            user_content_followup = get_text(language_code, 'generate_additional_narratives_user_content_followup', replacements={"selected_facts": ', '.join(selected_facts)})

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
 
    # Set primary narrative prompts to language code
    language_code = get_user_language_by_id(session['user_data']['user_id'])
    selected_facts = get_fact_combination_by_id(session['user_data']['fact_combination_id'])

    prompts = {
        "headline_system": get_text(language_code, 'generate_news_primary_system_content_headline', replacements={"selected_facts": ', '.join(selected_facts), "selected_narrative": selected_narrative}),
        "headline_user": get_text(language_code, 'generate_news_primary_user_content_headline', replacements={"selected_facts": ', '.join(selected_facts), "selected_narrative": selected_narrative}),
        # Note: The image prompt and story prompts are generated after the headline is created
    }

    # Call the function to generate news content
    news_data = generate_news_content(selected_narrative, prompts, selected_facts)

    # Return the news data as a JSON response
    return {"news_data": news_data}


def generate_news_content(selected_narrative, prompts, selected_facts):

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
    def generate_image(prompt):

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
            else:
                error_message = f"Failed to generate image. API Error: {response.status_code} - {response.text}"
                print(error_message)
                raise Exception(error_message)  

                # Check for content policy violation specifically
                if response.status_code == 400 and "content_policy_violation" in response.text:
                    raise Exception("Content policy violation detected. Adjusting the prompt may be necessary.")  
        except Exception as e:
            print(f"Network or request error occurred: {str(e)}")
            raise Exception(f"Network or request error occurred: {str(e)}")  

    # Generate headline
    headline = get_chatgpt_response(prompts['headline_system'], prompts['headline_user'])
    if headline is None:
        raise Exception("Failed to generate headline, halting process.")  

    # Update image prompt 
    language_code = get_user_language_by_id(session['user_data']['user_id']) 
    image_prompt = get_text(language_code, 'generate_news_primary_prompt_image', replacements={"headline": headline, "selected_narrative": selected_narrative}) 
    prompts['image'] = image_prompt  # Update the image prompt in the dictionary

    #Update story prompts
    prompts['story_system'] = get_text(language_code, 'generate_news_primary_system_content_story', replacements={"headline": headline, "selected_narrative": selected_narrative, "selected_facts": ', '.join(selected_facts)})
    prompts['story_user'] = get_text(language_code, 'generate_news_primary_user_content_story', replacements={"headline": headline, "selected_narrative": selected_narrative, "selected_facts": ', '.join(selected_facts)})

    # Generate story
    story = get_chatgpt_response(prompts['story_system'], prompts['story_user'])
    if story is None:
        raise Exception("Failed to generate story, halting process.")  

    # Generate image (based on the headline)
    image_url = generate_image(prompts['image'])

    # Combine the generated content
    news_content = {
        "headline": headline,
        "story": story,
        "image_url": image_url
    }
    
    return news_content



# def commit_primary_narrative_controller():

    # Store Primary Narrative ID in User Session
    # session['primary_narrative_id'] = selected_narrative

    # Commit Primary Narrative to Database
    # fact_combination_id = user_data(fact_combination_id)
    # narrative_text = get_primary_narrative_by_id(narrative_id):
    # user_id = user_data(user_id)
    # headline = newsjsonthing(headline)
    # story = newsjsonthing(story)
    # photo_url = newsjsonthing(photo_url)
    # create_primary_narrative(fact_combination_id, narrative_text, user_id, headline, story, photo_url)


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


