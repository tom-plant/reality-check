
# Function to get text based on language code, narrative context, and potentially multiple replacements
def get_text(language_code, category, context, key, replacements=None):
    localizations = {
        "ENG": ENG,
        "EST": EST,
        "RUS": RUS
    }

    # Retrieve the specifiers 
    localization = localizations.get(language_code, ENG)  
    category_prompts = localization.get(category, {})
    context_prompts = category_prompts.get(context, {})
    text = context_prompts.get(key, "Unknown key")

    # Replace placeholders with actual values if replacements are provided
    if replacements:
        for placeholder, replacement in replacements.items():
            text = text.replace(f"{{{placeholder}}}", str(replacement))

    return text


import json

# Load localizations from the JSON file
with open('localizations.json', 'r') as file:
    localizations = json.load(file)

# Function to get text based on language code, category, context, and key
def get_text(language_code, category, context, key, replacements=None):
    # Retrieve the specifiers 
    localization = localizations["prompts"].get(language_code, {})  
    category_prompts = localization.get(category, {})
    context_prompts = category_prompts.get(context, [])
    text_parts = context_prompts.get(key, ["Unknown key"])

    # Join the array elements to form the complete text
    text = '\n'.join(text_parts)

    # Replace placeholders with actual values if replacements are provided
    if replacements:
        for placeholder, replacement in replacements.items():
            text = text.replace(f"{{{placeholder}}}", str(replacement))

    return text
