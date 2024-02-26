# controllers.py
import random
import json
import requests
from db_operations import *
from config import API_KEY
from flask import session



def select_facts_controller(selected_facts):

    # Check if selected facts are associated with existing narratives, and how many
    narratives = get_narratives_by_fact_combination(selected_facts)
    num_narratives = len(narratives)

    # Check if there are 3 or more narratives and return only 3
    if num_narratives >= 3:
        random_narratives = random.sample(narratives, 3) if num_narratives > 3 else narratives
        return {"narratives": random_narratives}

    else:
        # Calculate the number of additional narratives needed
        num_additional_narratives = 3 - num_narratives

        # Generate additional narratives using ChatGPT API and combine with existing 
        additional_narratives = generate_additional_narratives(selected_facts, num_additional_narratives)
        combined_narratives = narratives + additional_narratives

        return {"narratives": combined_narratives}



def generate_additional_narratives(selected_facts, num_additional_narratives):

    # Call the ChatGPT API
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    narratives = []
    previous_narrative = None

    for i in range(num_additional_narratives):
        if i == 0 or num_additional_narratives == 1:
            print('generating with first prompt')

            # Use the initial prompt for the first narrative or if only one is needed
            system_content = "You are a senior level political analyst who writes in clear, understandable, and straightforward language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action."
            user_content = f"Craft your narrative based on the following information: {', '.join(selected_facts)}. It should be no more than three sentences."
        else:
            # Use the different prompt for subsequent narratives, referring back to the previous one
            print('generating with second prompt')
            system_content = previous_narrative
            user_content = f"Craft a narrative about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {', '.join(selected_facts)}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences."

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


def select_narrative_controller(selected_narrative, selected_facts):
    # Retrieve user_id from session
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "User not logged in"}, 401
 
    # Store selected narrative and facts in session for later use
    session['selected_narrative'] = selected_narrative
    session['selected_facts'] = selected_facts

    # Return a success response
    return {"message": "Narrative and facts selection processed successfully"}





def introduce_event_controller():
    # Logic to select and send randomly selected follow-up event to the frontend
    # Check if combination of previous narrative and event exists in the database
    # If exists, retrieve news headlines and photo from the database
    # If not, call ChatGPT API to generate news headlines and DALL-E 2 API to generate photo
    
    # Placeholder for now
    return jsonify({"message": "Introduce event controller placeholder"}) #TAKE OUT JSONIFY

# THis all comes in the event controller vvvv

    # # Placeholder for news generation logic
    # headline, news_story, photo = generate_news_content(selected_narrative)

# def generate_news_content(selected_narrative):
#     # Placeholder for the logic to generate news content
#     # This function should return headline, news_story, and photo based on the selected narrative
#     headline = "Generated Headline for " + selected_narrative
#     news_story = "Generated News Story for " + selected_narrative
#     photo = "Generated Photo URL for " + selected_narrative
#     return headline, news_story, photo

#    narrative_id = create_primary_narrative(selected_narrative, headline, news_story, photo, user_id)

#     # Update associations in NarrativeFactAssociation table
#     update_narrative_association(narrative_id, selected_facts)







def identify_weaknesses_controller(new_facts, narrative):
    # Logic to send new combination of facts and narrative to ChatGPT API to update with a new narrative and story outcome
    
    # Placeholder for now
    return jsonify({"message": "Identify weaknesses controller placeholder"}) #TAKE OUT JSONIFY


def save_progress_controller(user_progress):
    # Logic to save user progress data to the database
    
    # Placeholder for now
    return jsonify({"message": "Save progress controller placeholder"}) #TAKE OUT JSONIFY