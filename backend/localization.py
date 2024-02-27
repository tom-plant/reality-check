# English text
ENG = {
   
    "generate_additional_narratives_system_content": "You are a senior level political analyst who writes in clear, understandable, and straightforward language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
    "generate_additional_narratives_user_content": "Craft your narrative based on the following information: {facts}. It should be no more than three sentences.",
    "generate_additional_narratives_user_content_followup": "Craft a narrative about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
    "generate_news_primary_system_content_headline": "placeholder and info: {facts}",
    "generate_news_primary_user_content_headline": "placeholder and info: {facts}",
    "generate_news_primary_system_content_story": "placeholder and info: {facts}",
    "generate_news_primary_user_content_story": "placeholder and info: {facts}",
    "generate_news_primary_prompt_image": "placeholder and info: {facts}",
}

# Estonian text
EST = {

"generate_additional_narratives_system_content": "You are an Estonian senior level political analyst who writes in clear, understandable, and straightforward Estonian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative in the Estonian language using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
    "generate_additional_narratives_user_content": "Craft your narrative in Estonian based on the following information: {facts}. It should be no more than three sentences.",
    "generate_additional_narratives_user_content_followup": "Craft a narrative in Estonian about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
    "generate_news_primary_system_content_headline": "placeholder and info: {facts}",
    "generate_news_primary_user_content_headline": "placeholder and info: {facts}",
    "generate_news_primary_system_content_story": "placeholder and info: {facts}",
    "generate_news_primary_user_content_story": "placeholder and info: {facts}",
    "generate_news_primary_prompt_image": "placeholder and info: {facts}",
}

# Russian text
RUS = {

"generate_additional_narratives_system_content": "You are a Russian senior level political analyst who writes in clear, understandable, and straightforward Russian language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative in the Russian language using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
    "generate_additional_narratives_user_content": "Craft your narrative based on the following information: {facts}. It should be no more than three sentences.",
    "generate_additional_narratives_user_content_followup": "Craft a narrative in Russian about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {facts}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
    "generate_news_primary_system_content_headline": "placeholder and info: {facts}",
    "generate_news_primary_user_content_headline": "placeholder and info: {facts}",
    "generate_news_primary_system_content_story": "placeholder and info: {facts}",
    "generate_news_primary_user_content_story": "placeholder and info: {facts}",
    "generate_news_primary_prompt_image": "placeholder and info: {facts}",
}

# Function to get text based on language code
def get_text(language_code, key, facts=None):
    localization = {
        "ENG": ENG,
        "EST": EST,
        "RUS": RUS
    }.get(language_code, ENG)  # Default to English if the language code is not recognized

    text = localization.get(key, "Unknown key")
    if facts and "{facts}" in text:
        return text.format(facts=', '.join(facts))
    return text


# user_content = get_text(language_code, 'generate_additional_narratives_user_content', selected_facts)
