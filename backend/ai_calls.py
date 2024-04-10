# ai_calls.py

API_KEY = os.environ.get('API_KEY')

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
        "max_tokens": 300
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