# English text
EN = {
   
    "generate_additional_narratives_system_content": "You are a senior level political analyst who writes in clear, understandable, and straightforward language. Upon my submission of information to you, you must create a brief, distinct, actionable, and persuasive political narrative using the fact provided. It should stand alone and compete to define the event using the facts provided, even if in a biased way. It should lead the reader to a specific conclusion, opinion, or action.",
    "generate_additional_narratives_user_content": f"Craft your narrative based on the following information: {', '.join(selected_facts)}. It should be no more than three sentences.",
    "generate_additional_narratives_user_content_followup"; f"Craft a narrative about the event that leads to a competing conclusion or recommendation compared to the previous narrative, but whatever claim MUST be based on the following information: {', '.join(selected_facts)}. Any alternative course of action must come from the supplied information, and should be expressed without explicitly putting it in contrast with the last. It should be no more than three sentences.",
}

# Estonian text
EST = {

}

# Russian text
RUS = {


}

# Function to get text based on language code
def get_text(language_code, key):
    if language_code == "ENG":
        return EN.get(key, "Unknown key")
    elif language_code == "EST":
        return EST.get(key, "Unknown key")
    elif language_code == "RUS":
        return RUS.get(key, "Unknown key")
    else:
        return "Invalid language code"
