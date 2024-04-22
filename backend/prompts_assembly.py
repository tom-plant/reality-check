import json

def generate_prompts(file_path, category, prompt_type='both', dynamic_inserts=None):
    if dynamic_inserts is None:
        dynamic_inserts = {}

    # Load the prompts and inserts
    prompts_data = load_prompts_from_file(file_path)

    # For items that are lists (e.g., strategies), concatenate them into a single string
    for key, value in dynamic_inserts.items():
        if isinstance(value, list):
            dynamic_inserts[key] = ' '.join(value)

    # Combine static and dynamic inserts
    inserts = {**prompts_data.get('prompt_inserts', {}), **dynamic_inserts}

    assembled_prompts = {}

    # Fetch and assemble 'system' prompt if needed
    if prompt_type in ['both', 'system']:
        system_template = get_prompt_template(prompts_data, category, 'system')
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
        return prompts_data['prompts'][category][prompt_type]
    return None

def substitute_inserts(template, inserts):
    if not template:
        return None
    return template.format(**inserts)

def get_text(file_path, category, key, identifier=None):

    # Load the JSON data from the specified file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Navigate to the required text snippet based on the presence of an identifier
    try:
        if identifier:
            return data['prompt_inserts'][category][key][identifier]
        else:
            return data['prompt_inserts'][category][key]
    except KeyError:
        return f"Missing information: [{key}]"