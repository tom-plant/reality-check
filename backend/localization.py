# English text
ENG = {
    "chatgpt_prompts": {
        "additional_narratives": {
            "generate_additional_narratives_system_content": "You are a senior level political analyst who writes in clear, understandable, and straightforward language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative using the facts provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
            "generate_additional_narratives_user_content": "Craft your narrative based on the following information: {selected_facts}. It should be no more than three sentences.",
            "generate_additional_narratives_user_content_followup": "Craft a narrative about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {selected_facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
        },
        "primary_narrative": {
            "headline_system": "You write definitive and engaging headlines for newspapers.",
            "headline_user": "Write a headline about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
            "story_system": "You are a newspaper writer who writes stories in subtly biased ways, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
        },
        "events_narrative": {
            "headline_system": "You write definitive and engaging headlines for newspapers.",
            "headline_user": "Please write a headline for a breaking news event, '{selected_facts}', based on your previous position and opinion that is captured in this narrative, '{selected_narrative}'. You are looking to push forward this narrative in the context of the breaking news.",
            "story_system": "You are a newspaper writer who writes stories in subtly biased ways, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} is the breaking news event you are exploiting to push your narrative. Make sure your story weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
        }, 
        "secondary_narrative": {
            "secondary_system": "You are a senior level political analyst who writes in clear, understandable, and straightforward language. You write brief, distinct, actionable, and persuasive political narratives. However, you are in a situation where you must revise a faulty narrative you had written, simply because you did not have all the facts initially. You will receive updated evidence, and you must create a new revised narrative that leads to a different conclusion based on the new information you now have. Your new narrative should stand alone and seek to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action. It should be short and straightforward with a clear implication.",
            "secondary_user": "Your initial narrative was this: {selected_narrative}. Now, craft your NEW standalone, replacement narrative that leads to a different logical conclusion based on the following information: {selected_facts}. Your new narrative should be no more than three sentences. Don't mention that it's new. Treat it like a replacement. It should be about a sentence long. Short and straightforward.",
            "headline_system": "You write definitive and engaging headlines for newspapers.",
            "headline_user": "Write a headline about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
            "story_system": "You are a newspaper writer who writes stories in subtly biased ways, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences.",
            "image_prompt": "Please generate a realistic, news photo to accompany an article. {headline} is the headline.",
            "ending_prompt": ""
        },
    },
}#             "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture. If this prompt is too intense, scale back the image so it doesn't include anything that would violate the content guidelines.",


# Estonian text
EST = {
    "chatgpt_prompts": {
        "additional_narratives": {
            "generate_additional_narratives_system_content": "You are an Estonian senior level political analyst who writes in clear, understandable, and straightforward Estonian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative in the Estonian language using the facts provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
            "generate_additional_narratives_user_content": "Craft your narrative in Estonian based on the following information: {selected_facts}. It should be no more than three sentences.",
            "generate_additional_narratives_user_content_followup": "Craft a narrative in Estonian about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {selected_facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
        },
        "primary_narrative": {
            "headline_system": "You write definitive and engaging headlines for newspapers in Estonian.",
            "headline_user": "Write a headline in Estonian about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
            "story_system": "You are an Estonian newspaper writer who writes stories in subtly biased ways using the Estonian language, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences and write in Estonian.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
        },
        "events_narrative": {
            "headline_system": "You write definitive and engaging headlines for newspapers in Estonian.",
            "headline_user": "Please write a headline in Estonian for a breaking news event, '{selected_facts}', based on your previous position and opinion that is captured in this narrative, '{selected_narrative}'. You are looking to push forward this narrative in the context of the breaking news.",
            "story_system": "You are an Estonian newspaper writer who writes stories in subtly biased ways using the Estonian language, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} is the breaking news event you are exploiting to push your narrative. Make sure your story weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences in Estonian.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
        }, 
        "secondary_narrative": {
            "secondary_system": "You are an Estonian senior level political analyst who writes in clear, understandable, and straightforward Estonian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative  in the Estonian language using the facts provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
            "secondary_user": "Craft your narrative in Estonian based on the following information: {selected_facts}. It should be no more than three sentences.",
            "headline_system": "You write definitive and engaging headlines for newspapers in Estonian.",
            "headline_user": "Write a headline in Estonian about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
            "story_system": "You are an Estonian newspaper writer who writes stories in subtly biased ways using the Estonian language, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences in Estonian.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
            "ending_prompt": ""
        }, 
    },
}

# Russian text
RUS = {
    "chatgpt_prompts": {
        "additional_narratives": {
            "generate_additional_narratives_system_content": "You are a Russian senior level political analyst who writes in clear, understandable, and straightforward Russian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative in the Russian language using the facts provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
            "generate_additional_narratives_user_content": "Craft your narrative based on the following information: {selected_facts}. It should be no more than three sentences.",
            "generate_additional_narratives_user_content_followup": "Craft a narrative in Russian about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {selected_facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
        },
        "primary_narrative": {
            "headline_system": "You write definitive and engaging headlines for newspapers in Russian.",
            "headline_user": "Write a headline in Russian about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
            "story_system": "You are a Russian newspaper writer who writes stories in subtly biased ways using the Russian language, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences and write in Russian.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
        },
        "events_narrative": {
            "headline_system": "You write definitive and engaging headlines for newspapers in Russian.",
            "headline_user": "Please write a headline in Russian for a breaking news event, '{selected_facts}', based on your previous position and opinion that is captured in this narrative, '{selected_narrative}'. You are looking to push forward this narrative in the context of the breaking news.",
            "story_system": "You are a Russian newspaper writer who writes stories in subtly biased ways using the Russian language, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} is the breaking news event you are exploiting to push your narrative. Make sure your story weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences in Russian.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
        }, 
        "secondary_narrative": {
            "secondary_system": "You are a Russian senior level political analyst who writes in clear, understandable, and straightforward Russian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative  in the Estonian language using the facts provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
            "secondary_user": "Craft your narrative in Russian based on the following information: {selected_facts}. It should be no more than three sentences.",
            "headline_system": "You write definitive and engaging headlines for newspapers in Russian.",
            "headline_user": "Write a headline in Russian about the following narrative: {selected_narrative}. For context, this narrative came from the following information: {selected_facts}.",
            "story_system": "You are an Estonian newspaper writer who writes stories in subtly biased ways using the Russian language, meaning that you may overlook the broader context to push a narrative.",
            "story_user": "{headline} is the headline to your story. {selected_narrative} is the narrative you're pushing, and {selected_facts} are your main evidence, but make sure it weaves that information together in a story with a relevant news hook to set the scene. Keep it around 5-6 sentences in Russian.",
            "image_prompt": "Please generate a realistic, photojournalism image to accompany a news article. {headline} is the headline and '{selected_narrative}' is the story your photograph should capture.",
            "ending_prompt": ""
        }, 
    },
}


# Function to get text based on language code, narrative context, and potentially multiple replacements
def get_text(language_code, category, context, key, replacements=None):
    localizations = {
        "ENG": ENG,
        "EST": EST,
        "RUS": RUS
    }

    # Default to English if the language code is not recognized
    localization = localizations.get(language_code, ENG)  

    # Retrieve the category-specific prompts (e.g., chatgpt_prompts)
    category_prompts = localization.get(category, {})

    # Retrieve the context-specific prompts within the category
    context_prompts = category_prompts.get(context, {})

    # Retrieve the specific prompt by key within the context
    text = context_prompts.get(key, "Unknown key")

    # Replace placeholders with actual values if replacements are provided
    if replacements:
        for placeholder, replacement in replacements.items():
            text = text.replace(f"{{{placeholder}}}", replacement)

    return text


# Example Usage

# language_code = "ENG"
# category = "chatgpt_prompts"
# context = "additional_narratives"
# key = "generate_additional_narratives_user_content"
# replacements = {
#     "selected_facts": "rising unemployment rates, increased inflation"
# }

# prompt = get_text(language_code, category, context, key, replacements)
# print(prompt)
