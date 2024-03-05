# English text
ENG = {
   
    # Generative AI Prompts

    # Additional Narrative Prompts
    "generate_additional_narratives_system_content": "You are a senior level political analyst who writes in clear, understandable, and straightforward language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
    "generate_additional_narratives_user_content": "Craft your narrative based on the following information: {selected_facts}. It should be no more than three sentences.",
    "generate_additional_narratives_user_content_followup": "Craft a narrative about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {selected_facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",

    # Primary Narrative Prompts
    "generate_news_primary_system_content_headline": "You write definitive and engaging headlines for newpapers.",
    "generate_news_primary_user_content_headline": "Write a headline about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
    "generate_news_primary_system_content_story": "You are a newspaper writer who writes stories in subtly biased ways, meaning that you may overlook the broader context to push a narrative.",
    "generate_news_primary_user_content_story": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences.",
    "generate_news_primary_prompt_image": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
    
    # Event Narrative Prompts
    "generate_news_events_system_content_headline": "You write definitive and engaging headlines for newpapers.",
    "generate_news_events_user_content_headline": "Please write a headline for a breaking news event, '{selected_facts}', based on your previous position and opinion that is captured in this narrative, '{selected_narrative}'. You are looking to push forward this narrative in the context of the breaking news.",
    "generate_news_events_system_content_story": "You are a newspaper writer who writes stories in subtly biased ways, meaning that you may overlook the broader context to push a narrative.",
    "generate_news_events_user_content_story": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} is the breaking news event you are exploiting to push your narrative. Make sure your story weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences.",
    "generate_news_events_prompt_image": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
}

# Estonian text
EST = {

    # Generative AI Prompts

    # Additional Narrative Prompts
    "generate_additional_narratives_system_content": "You are an Estonian senior level political analyst who writes in clear, understandable, and straightforward Estonian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative in the Estonian language using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
    "generate_additional_narratives_user_content": "Craft your narrative in Estonian based on the following information: {selected_facts}. It should be no more than three sentences.",
    "generate_additional_narratives_user_content_followup": "Craft a narrative in Estonian about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {selected_facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
    
    # Primary Narrative Prompts
    "generate_news_primary_system_content_headline": "You write definitive and engaging headlines for newpapers in Estonian.",
    "generate_news_primary_user_content_headline": "Write a headline in Estonian about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
    "generate_news_primary_system_content_story": "You are an Estonian newspaper writer who writes stories in subtly biased ways using the Estonian language, meaning that you may overlook the broader context to push a narrative.",
    "generate_news_primary_user_content_story": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences and write in Estonian.",
    "generate_news_primary_prompt_image": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
    
    # Event Narrative Prompts
    "generate_news_events_system_content_headline": "You write definitive and engaging headlines for newpapers in Estonian.",
    "generate_news_events_user_content_headline": "Please write a headline in Estonian for a breaking news event, '{selected_facts}', based on your previous position and opinion that is captured in this narrative, '{selected_narrative}'. You are looking to push forward this narrative in the context of the breaking news.",
    "generate_news_events_system_content_story": "You are an Estonian newspaper writer who writes stories in subtly biased ways using the Estonian language, meaning that you may overlook the broader context to push a narrative.",
    "generate_news_events_user_content_story": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} is the breaking news event you are exploiting to push your narrative. Make sure your story weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences in Estonian.",
    "generate_news_events_prompt_image": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
}

# Russian text
RUS = {

    # Generative AI Prompts
    
    # Additional Narrative Prompts
    "generate_additional_narratives_system_content": "You are a Russian senior level political analyst who writes in clear, understandable, and straightforward Russian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative in the Russian language using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
    "generate_additional_narratives_user_content": "Craft your narrative based on the following information: {selected_facts}. It should be no more than three sentences.",
    "generate_additional_narratives_user_content_followup": "Craft a narrative in Russian about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {selected_facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
    
    # Primary Narrative Prompts
    "generate_news_primary_system_content_headline": "You write definitive and engaging headlines for newpapers in Russian.",
    "generate_news_primary_user_content_headline": "Write a headline in Russian about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
    "generate_news_primary_system_content_story": "You are a Russian newspaper writer who writes stories in subtly biased ways using the Russian language, meaning that you may overlook the broader context to push a narrative.",
    "generate_news_primary_user_content_story": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences and write in Russian.",
    "generate_news_primary_prompt_image": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
    
    # Event Narrative Prompts
    "generate_news_events_system_content_headline": "You write definitive and engaging headlines for newpapers in Russian.",
    "generate_news_events_user_content_headline": "Please write a headline in Russian for a breaking news event, '{selected_facts}', based on your previous position and opinion that is captured in this narrative, '{selected_narrative}'. You are looking to push forward this narrative in the context of the breaking news.",
    "generate_news_events_system_content_story": "You are a Russian newspaper writer who writes stories in subtly biased ways using the Russian language, meaning that you may overlook the broader context to push a narrative.",
    "generate_news_events_user_content_story": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} is the breaking news event you are exploiting to push your narrative. Make sure your story weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences in Russian.",
    "generate_news_events_prompt_image": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
}


# Function to get text based on language code and potentially multiple replacements
def get_text(language_code, key, replacements=None):
    localization = {
        "ENG": ENG,
        "EST": EST,
        "RUS": RUS
    }.get(language_code, ENG)  # Default to English if the language code is not recognized

    text = localization.get(key, "Unknown key")
    if replacements:
        for placeholder, replacement in replacements.items():
            placeholder_pattern = "{" + placeholder + "}"
            if placeholder_pattern in text:
                text = text.replace(placeholder_pattern, replacement)
    return text

