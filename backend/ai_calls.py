# ai_calls.py

import json
import requests
import os

API_KEY = os.environ.get('API_KEY')


def get_chatgpt_response(prompts):
    # ChatGPT API settings
    chatGPTUrl = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Construct the messages payload
    messages = []
    if 'system' in prompts:
        messages.append({"role": "system", "content": prompts['system']})
    if 'user' in prompts:
        messages.append({"role": "user", "content": prompts['user']})

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 500
    }

    try:
        response = requests.post(chatGPTUrl, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            error_message = f"Failed to generate text content. API Error: {response.status_code} - {response.text}"
            return {"error": error_message}
    except Exception as e:
        error_message = f"Network or request error occurred: {str(e)}"
        return {"error": error_message}


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
        response.raise_for_status()  # Raise HTTPError for bad responses

        image_data = response.json().get('data')
        if image_data:
            return image_data[0].get('url')
        else:
            return {"error": "No image data returned from DALL-E API"}
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            error_info = response.json().get('error', {})
            if error_info.get('code') == 'content_policy_violation':
                return {"error": "Content policy violation detected."}
            else:
                return {"error": f"Failed to generate image. API Error: {response.status_code} - {response.text}"}
        else:
            return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}