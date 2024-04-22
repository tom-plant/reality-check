import json
import logging
import json
import requests
from flask import  current_app
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_prompts( category, prompt_type='both', dynamic_inserts=None):

    file_path = '/app/backend/prompts.json'

    if dynamic_inserts is None:
        dynamic_inserts = {}

    # Load the prompts and inserts
    prompts_data = load_prompts_from_file(file_path)

    # For items that are lists (e.g., strategies), concatenate them into a single string
    for key, value in dynamic_inserts.items():
        if isinstance(value, list):
            dynamic_inserts[key] = ' '.join(value)

    # Combine static and dynamic inserts
    current_app.logger.debug("Dynamic Inserts:", dynamic_inserts)
    inserts = {**prompts_data.get('prompt_inserts', {}), **dynamic_inserts}
    current_app.logger.debug("Combined Inserts before substitution:", inserts)

    assembled_prompts = {}

    # Fetch and assemble 'system' prompt if needed
    if prompt_type in ['both', 'system']:
        system_template = get_prompt_template(prompts_data, category, 'system')
        if system_template:  # Check if template is not None
            assembled_prompts['system'] = substitute_inserts(system_template, inserts)

    # Fetch and assemble 'user' prompt if needed
    if prompt_type in ['both', 'user'] and 'user' in prompts_data['prompts'].get(category, {}):
        user_template = get_prompt_template(prompts_data, category, 'user')
        assembled_prompts['user'] = substitute_inserts(user_template, inserts)

    # For categories with only a 'system' prompt, handle accordingly
    if category in ['news_photo', 'youtube_thumbnail'] and 'system' in assembled_prompts:
        return assembled_prompts['system']

    return assembled_prompts

def load_prompts_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_prompt_template(prompts_data, category, prompt_type='system'):
    if category in prompts_data['prompts'] and prompt_type in prompts_data['prompts'][category]:
        template = prompts_data['prompts'][category][prompt_type]
        if isinstance(template, list):
            # Join the list into a single string with spaces or newlines as appropriate
            return ' '.join(template)
        return template  # This will be a string if not a list
    return None  # Return None if the category or type is not found

def substitute_inserts(template, inserts):
    if not template:
        return None  # Handle None case explicitly to avoid formatting errors
    try:
        return template.format(**inserts)
    except KeyError as e:
        return "Error: Missing key {}".format(e)  # Provide error detail in output

def get_text(category, key, identifier=None):

    file_path = '/app/backend/prompts.json'

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        if identifier:
            return data['prompt_inserts'][category][key][identifier]
        else:
            return data['prompt_inserts'][category][key]
    except KeyError:
        return f"Missing information: [{key}]"
    except FileNotFoundError:
        return "Error: The file 'prompts.json' was not found."
    except Exception as e:
        return f"An error occurred: {e}"