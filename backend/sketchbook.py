

#NEWS ARTICLE

prompts_news_article = generate_prompts(
    file_path='prompts.json',
    category='news_article',
    prompt_type='both',
    dynamic_inserts={
        'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
    }
)



#NEWS PHOTO

# Assuming 'headline' is defined
prompts_news_photo = generate_prompts(
    file_path='prompts.json',
    category='news_photo',
    prompt_type='system',
    dynamic_inserts={
        'headline': headline
    }
)


#SOCIAL MEDIA CONTENT

prompts_social_media_content = generate_prompts(
    file_path='prompts.json',
    category='social_media_content',
    prompt_type='both',
    dynamic_inserts={
        'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
        'facts': get_fact_combination_by_id(session['user_data']['fact_combination_id']),
    }
)

#YOUTUBE THUMBNAIL

# Assuming 'video_title' is defined
prompts_youtube_thumbnail = generate_prompts(
    file_path='prompts.json',
    category='youtube_thumbnail',
    prompt_type='system',
    dynamic_inserts={
        'video_title': video_title
    }
)



#EVENT OUTCOMES

# Assuming 'event' and 'outcomes' are defined
prompts_event_outcomes = generate_prompts(
    file_path='prompts.json',
    category='event_outcome',
    prompt_type='both',
    dynamic_inserts={
        'event': event,
        'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
    }
)


#COUNTERNARRATIVE

# Assuming 'selected_strategies', 'updated_facts', and necessary functions are defined
prompts_counter_narrative = {}
for strategy in selected_strategies:
    prompts_counter_narrative[strategy] = generate_prompts(
        file_path='prompts.json',
        category='counter_narrative',
        prompt_type='both',
        dynamic_inserts={
            'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
            'updated_facts': updated_facts,
            'strategy': get_text('prompt_inserts', 'strategy', strategy)
        }
    )


#ELECTION OUTCOMES

prompts_election_outcomes = generate_prompts(
    file_path='prompts.json',
    category='election_outcome',
    prompt_type='both',
    dynamic_inserts={
        'narrative': get_primary_narrative_by_id(session['user_data']['primary_narrative_id']),
        'counter_narrative': get_secondary_narrative_by_id(session['user_data']['secondary_narrative_id']),
        'crisis_background': get_text('plot_context', 'crisis_background'),
    }
)






















def generate_prompts(category, sub_category, needs_user_prompt=True, **kwargs):
    system_prompt = get_text('prompts', sub_category, 'system', **kwargs)

    # Initialize a dictionary to hold the prompts
    prompt_data = {'system': system_prompt}

    # Check if a user prompt is needed
    if needs_user_prompt:
        user_prompt = get_text('prompts', sub_category, 'user', **kwargs)
        prompt_data['user'] = user_prompt

    return prompt_data

def get_text(main_category, sub_category, prompt_type=None, **replacements):
    # Load the prompts from the JSON file
    with open('prompts.json', 'r') as file:
        prompts = json.load(file)

    text = prompts[main_category][sub_category]
    if prompt_type:
        text = text[prompt_type]

    # Use string formatting to replace placeholders with actual content
    return text.format(**replacements)