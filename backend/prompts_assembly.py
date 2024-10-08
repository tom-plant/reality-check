import json
import logging
import requests
from flask import current_app
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_prompts( category, prompt_type='both', dynamic_inserts=None):

    file_path = '/app/backend/prompts.json'

    if dynamic_inserts is None:
        dynamic_inserts = {}

    # Load the prompts and inserts
    prompts_data = load_prompts_from_file(file_path)
    construction_strategies = prompts_data.get('prompt_inserts', {}).get('construction_strategies', {})
    counter_strategies = prompts_data.get('prompt_inserts', {}).get('counter_strategies', {})

    # For items that are lists (e.g., strategies), concatenate them into a single string
    for key, value in dynamic_inserts.items():
        if isinstance(value, list):
            dynamic_inserts[key] = ' '.join(value)

    # Convert the verbose strategy description to a key
    if 'strategy' in dynamic_inserts:
        current_app.logger.debug(f"Original strategy description received: {dynamic_inserts['strategy']}")
        strategy_key = map_strategy_to_key(dynamic_inserts['strategy'])
        detailed_strategy = ' '.join(construction_strategies.get(strategy_key, ["Strategy not found"]))
        current_app.logger.debug(f"Detailed strategy fetched for key '{strategy_key}': {detailed_strategy}")
        dynamic_inserts['strategy'] = detailed_strategy

    # Convert the verbose counterstrategy descrption to a key
    if 'counter_strategy'in dynamic_inserts:
        current_app.logger.debug(f"Original strategy description received: {dynamic_inserts['counter_strategy']}")
        counter_strategy_key = map_strategy_to_key(dynamic_inserts['counter_strategy'])
        detailed_counter_strategy = ' '.join(counter_strategies.get(counter_strategy_key, ["Counter strategy not found"]))
        current_app.logger.debug(f"Detailed strategy fetched for key '{counter_strategy_key}': {detailed_counter_strategy}")
        dynamic_inserts['counter_strategy'] = detailed_counter_strategy


    # Combine static and dynamic inserts
    # current_app.logger.debug("Dynamic Inserts:", dynamic_inserts)
    inserts = {**prompts_data.get('prompt_inserts', {}), **dynamic_inserts}
    current_app.logger.debug("Combined Inserts before substitution:", inserts)

    assembled_prompts = {}

    # Fetch and assemble 'system' prompt if needed
    if prompt_type in ['both', 'system', 'user_followup']:  # Include 'user_followup' to fetch 'system'
        system_template = get_prompt_template(prompts_data, category, 'system')
        if system_template:  # Check if template is not None
            assembled_prompts['system'] = substitute_inserts(system_template, inserts)

    # Fetch and assemble 'user' prompt if needed
    if prompt_type in ['both', 'user'] and 'user' in prompts_data['prompts'].get(category, {}):
        user_template = get_prompt_template(prompts_data, category, 'user')
        assembled_prompts['user'] = substitute_inserts(user_template, inserts)

    # Fetch and assemble 'user_followup' prompt if needed
    if prompt_type in ['user_followup']:  # Exclusive handling for 'user_followup'
        followup_template = get_prompt_template(prompts_data, category, 'user_followup')
        if followup_template:
            assembled_prompts['user_followup'] = substitute_inserts(followup_template, inserts)

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
    
def map_strategy_to_key(verbose_description):
    strategy_map = {
        "Showing the Cause-and-Effect: Saying one event caused another without sufficient detail to connect the two events.": "causal_chain",
        "Instructing What to Believe: Directly telling the reader what is correct and incorrect.": "instruct_belief",
        "Highlighting Danger: Focusing on risks to guide readers to a belief based on emotions, like fear.": "highlight_danger",
        "Appealing to Personal Beliefs: Connecting the reader’s existing beliefs to a particular understanding of an event.": "appeal_beliefs",
        "Offering an Alternative Explanation: Presenting an alternative explanation to the inaccurate one without explicitly correcting it.": "logic_based",
        "Debunking the False Claim: Providing thorough reasoning to disprove misleading information.": "fact_based",
        "Recalibrating Emotions and Framing: Using a correction to validate the reader's existing beliefs and reassure their interests.": "emotion_based",
        "Corrective Data Aligned with Personal Values: Offering data and evidence from trusted sources to back up true claims.": "source_based"
    }
    verbose_description = verbose_description.strip()
    matched_key = strategy_map.get(verbose_description, "default_key_if_not_found")
    current_app.logger.debug(f"Mapping verbose description '{verbose_description}' to key '{matched_key}'")
    return matched_key
