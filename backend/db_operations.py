# db_operations.py

from sqlalchemy import select, func, and_, or_
import os
from backend.database import db
from backend.models import User, Fact, Event, Actor, Strat, Strat, CounterStrat, StrategyEffectiveness, FactCombination, PrimaryNarrative, NarrativeEvent, SecondaryNarrative

# User Operations

# Create a New User
def create_user(username, email, _session=None):
    session = _session or db.session
    new_user = User(username=username, email=email)
    session.add(new_user)
    if not _session:  # Commit only if not using an external session
        try:
            session.commit()
            return new_user
        except Exception as e:
            session.rollback()
            raise e
    else:
        return new_user  # Return the user object without committing if using an external session

# Read Users
def get_user_by_id(user_id, _session=None):
    session = _session or db.session
    return session.get(User, user_id)

def get_all_users(_session=None):
    session = _session or db.session
    return session.execute(select(User)).scalars().all()

def get_user_by_username(username, _session=None):
    session = _session or db.session
    return session.execute(select(User).filter_by(username=username)).scalars().first()

def get_user_by_username_or_email(username_or_email, _session=None):
    session = _session or db.session
    user = session.execute(
        select(User).where(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        )
    ).scalars().first()
    return user

def get_user_by_email(email, _session=None):
    session = _session or db.session
    user = session.execute(
        select(User).where(User.email == email)
    ).scalars().first()
    return user

def get_user_language_by_id(user_id, _session=None):
    session = _session or db.session
    user = session.get(User, user_id)
    return user.language if user else None

# Update a User
def update_user(user_id, _session=None, **kwargs):
    session = _session or db.session
    user = session.get(User, user_id)
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return user
            except Exception as e:
                session.rollback()
                raise e
        else:
            return user  # Return the user object without committing if using an external session


#Delete a User
def delete_user(user_id, _session=None):
    session = _session or db.session
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return True  # Assume deletion is successful if using an external session

#CounterStrat Operations

def get_all_counterstrats(_session=None):
    session = _session or db.session
    return session.execute(select(CounterStrat)).scalars().all()

def get_counter_strategy_id_by_name(strategy_name):
    strategy_name = strategy_name.strip()
    counter_strategy = CounterStrat.query.filter(CounterStrat.text.ilike(strategy_name)).first()
    return counter_strategy.id if counter_strategy else None

# Strat Operations

def get_all_strats(_session=None):
    session = _session or db.session
    return session.execute(select(Strat)).scalars().all()

def get_strategy_id_by_strategy_name(strategy_name):
    strategy = Strat.query.filter_by(text=strategy_name).first()
    return strategy.id if strategy else None

# StrategyEffectiveness Operations

def get_effectiveness_by_ids(strategy_id, counter_strategy_id):
    """
    Retrieve the effectiveness of a strategy and counter-strategy matchup using their IDs.

    Args:
        strategy_id (int): The ID of the strategy.
        counter_strategy_id (int): The ID of the counter-strategy.

    Returns:
        str: The effectiveness rating ('strong', 'medium', 'weak').
    """
    effectiveness_record = StrategyEffectiveness.query.filter_by(
        strategy_id=strategy_id,
        counter_strategy_id=counter_strategy_id
    ).first()
    return effectiveness_record.effectiveness if effectiveness_record else 'medium'


# Actor Operations

def get_all_actors(_session=None):
    session = _session or db.session
    return session.execute(select(Actor)).scalars().all()

def get_actor_id_by_actor_name(name):
    # name = name.strip().lower()
    actor = Actor.query.filter_by(text=name).first()
    return actor.id if actor else None

# Fact Operations

# Create a New Fact
def create_fact(text, language, _session=None):
    session = _session or db.session
    new_fact = Fact(text=text, language=language)
    session.add(new_fact)
    if not _session:  # Commit only if not using an external session
        try:
            session.commit()
            return new_fact
        except Exception as e:
            session.rollback()
            raise e
    else:
        return new_fact  # Return the fact object without committing if using an external session

# Read Facts
def get_fact_by_id(fact_id, _session=None):
    session = _session or db.session
    return session.get(Fact, fact_id)

def get_all_facts(_session=None):
    session = _session or db.session
    return session.execute(select(Fact)).scalars().all()

def get_facts_by_language(language, _session=None):
    session = _session or db.session
    return session.execute(select(Fact).filter_by(language=language)).scalars().all()


# Update a Fact
def update_fact(fact_id, _session=None, **kwargs):
    session = _session or db.session
    fact = session.get(Fact, fact_id)
    if fact:
        for key, value in kwargs.items():
            setattr(fact, key, value)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return fact
            except Exception as e:
                session.rollback()
                raise e
        else:
            return fact  # Return the fact object without committing if using an external session

# Delete a Fact
def delete_fact(fact_id, _session=None):
    session = _session or db.session
    fact = session.get(Fact, fact_id)
    if fact:
        session.delete(fact)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return True  # Assume deletion is successful if using an external session



# Event Operations

# Create a New Event
def create_event(text, language, _session=None):
    session = _session or db.session
    new_event = Event(text=text, language=language)
    session.add(new_event)
    if not _session:  # Commit only if not using an external session
        try:
            session.commit()
            return new_event
        except Exception as e:
            session.rollback()
            raise e
    else:
        return new_event  # Return the event object without committing if using an external session

# Read Events
def get_event_by_id(event_id, _session=None):
    session = _session or db.session
    return session.get(Event, event_id)

def get_all_events(_session=None):
    session = _session or db.session
    return session.execute(select(Event)).scalars().all()

def get_events_by_language(language, _session=None):
    session = _session or db.session
    return session.execute(select(Event).filter_by(language=language)).scalars().all()

def get_random_event(_session=None):
    session = _session or db.session
    return session.query(Event).order_by(func.random()).first()


# Update an Event
def update_event(event_id, _session=None, **kwargs):
    session = _session or db.session
    event = session.get(Event, event_id)
    if event:
        for key, value in kwargs.items():
            setattr(event, key, value)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return event
            except Exception as e:
                session.rollback()
                raise e
        else:
            return event  # Return the event object without committing if using an external session


# Delete an Event
def delete_event(event_id, _session=None):
    session = _session or db.session
    event = session.get(Event, event_id)
    if event:
        session.delete(event)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return True  # Assume deletion is successful if using an external session


#Fact Combination Operations

# Create a New Fact Combination
def create_fact_combination(facts, _session=None):
    session = _session or db.session
    new_fact_combination = FactCombination(facts=facts)  # Assuming `facts` is appropriately formatted
    session.add(new_fact_combination)
    if not _session:  # Commit only if not using an external session
        try:
            session.commit()
            return new_fact_combination
        except Exception as e:
            session.rollback()
            raise e
    else:
        return new_fact_combination  # Return the object without committing if using an external session


# Read Fact Combinations
def get_fact_combination_by_id(fact_combination_id, _session=None):
    session = _session or db.session
    fact_combination = session.get(FactCombination, fact_combination_id)
    if fact_combination:
        return fact_combination.facts  # Return just the facts string or JSON
    return None  # Return None if the FactCombination object was not found

def get_all_fact_combinations(_session=None):
    session = _session or db.session
    return session.execute(select(FactCombination)).scalars().all()

def count_fact_combinations(_session=None):
    session = _session or db.session
    count = session.query(FactCombination).count()
    return count


# Update a Fact Combination
def update_fact_combination(fact_combination_id, facts, _session=None):
    session = _session or db.session
    fact_combination = session.get(FactCombination, fact_combination_id)
    if fact_combination:
        fact_combination.facts = facts  # Ensure `facts` is correctly formatted
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return fact_combination
            except Exception as e:
                session.rollback()
                raise e
        else:
            return fact_combination  # Return the object without committing if using an external session


#Delete a Fact Combination
def delete_fact_combination(fact_combination_id, _session=None):
    session = _session or db.session
    fact_combination = session.get(FactCombination, fact_combination_id)
    if fact_combination:
        session.delete(fact_combination)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return True  # Assume deletion is successful if using an external session

# Retrieve Narratives By Fact Combination ID
def get_narratives_by_fact_combination(fact_combination_id, _session=None):
    session = _session or db.session
    
    # Directly retrieve narratives associated with the fact_combination_id
    primary_narratives = session.execute(
        select(PrimaryNarrative).where(PrimaryNarrative.fact_combination_id == fact_combination_id)
    ).scalars().all()

    return primary_narratives

# Retrieve Fact ID by Fact Combination
def get_fact_combination_id_by_facts(facts, _session=None):
    session = _session or db.session

    # Convert the input facts list to a set for efficient comparison
    input_facts_set = set(facts)

    # Retrieve all fact combinations
    all_fact_combinations = session.query(FactCombination).all()

    for fact_combination in all_fact_combinations:
        # Split the stored comma-separated facts string into a list and convert to a set
        stored_facts_set = set(fact_combination.facts.split(','))

        # Check if the sets are equal, indicating a match regardless of order
        if stored_facts_set == input_facts_set:
            return fact_combination.id  # Return the matching FactCombination ID

    return None  # Return None if no matching FactCombination is found


# Primary Narrative Operations

# Create a New Primary Narrative
def create_primary_narrative(fact_combination_id, narrative_text, user_id, actor_id, strat_id, news, _session=None):
    session = _session or db.session
    new_primary_narrative = PrimaryNarrative(
        fact_combination_id=fact_combination_id,
        narrative_text=narrative_text,
        user_id=user_id,
        actor_id=actor_id,
        strat_id=strat_id,
        news=news,
    )
    session.add(new_primary_narrative)
    if not _session:  # Commit only if not using an external session
        try:
            session.commit()
            return new_primary_narrative
        except Exception as e:
            session.rollback()
            raise e
    else:
        return new_primary_narrative  # Return the narrative object without committing if using an external session

# Read Primary Narrative
def get_primary_narrative_by_id(narrative_id, _session=None):
    session = _session or db.session
    return session.get(PrimaryNarrative, narrative_id)

def get_all_primary_narratives(_session=None):
    session = _session or db.session
    return session.execute(select(PrimaryNarrative)).scalars().all()

def get_primary_narratives_by_user(user_id, _session=None):
    session = _session or db.session
    return session.execute(select(PrimaryNarrative).filter_by(user_id=user_id)).scalars().all()


# Update a Primary Narrative
def update_primary_narrative(narrative_id, _session=None, **kwargs):
    session = _session or db.session
    primary_narrative = session.get(PrimaryNarrative, narrative_id)
    if primary_narrative:
        for key, value in kwargs.items():
            setattr(primary_narrative, key, value)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return primary_narrative
            except Exception as e:
                session.rollback()
                raise e
        else:
            return primary_narrative  # Return the narrative object without committing if using an external session

# Delete a Primary Narrative
def delete_primary_narrative(narrative_id, _session=None):
    session = _session or db.session
    primary_narrative = session.get(PrimaryNarrative, narrative_id)
    if primary_narrative:
        session.delete(primary_narrative)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return True  # Assume deletion is successful if using an external session


# Narrative Event Operations

# Create A New Narrative-Event Pair
def create_narrative_event(narrative_id, event_id, resulting_headline=None, resulting_story=None, resulting_photo_url=None, _session=None):
    session = _session or db.session
    new_narrative_event = NarrativeEvent(
        narrative_id=narrative_id,
        event_id=event_id,
        resulting_headline=resulting_headline,
        resulting_story=resulting_story,
        resulting_photo_url=resulting_photo_url
    )
    session.add(new_narrative_event)
    if not _session:  # Commit only if not using an external session
        try:
            session.commit()
            return new_narrative_event
        except Exception as e:
            session.rollback()
            raise e
    else:
        return new_narrative_event  # Return the narrative-event pair object without committing if using an external session


# Read Narrative-Event Pair
def get_narrative_events_by_id(narrative_events_id, _session=None):
    session = _session or db.session
    return session.get(NarrativeEvent, narrative_events_id)

def get_all_narrative_events(_session=None):
    session = _session or db.session
    return session.execute(select(NarrativeEvent)).scalars().all()

def get_narrative_events_by_narrative(narrative_id, _session=None):
    session = _session or db.session
    return session.execute(select(NarrativeEvent).filter_by(narrative_id=narrative_id)).scalars().all()

def get_news_content_by_narrative_events_id(narrative_events_id, _session=None):
    session = _session or db.session
    result = session.query(NarrativeEvent)\
        .filter(NarrativeEvent.id == narrative_events_id)\
        .with_entities(NarrativeEvent.resulting_headline, NarrativeEvent.resulting_story, NarrativeEvent.resulting_photo_url)\
        .first()

    if result:
        return {
            'headline': result.resulting_headline,
            'story': result.resulting_story,
            'photo_url': result.resulting_photo_url
        }
    else:
        return None


# Update a Narrative-Event Pair
def update_narrative_event(narrative_events_id, _session=None, **kwargs):
    session = _session or db.session
    narrative_event = session.get(NarrativeEvent, narrative_events_id)
    if narrative_event:
        for key, value in kwargs.items():
            setattr(narrative_event, key, value)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return narrative_event
            except Exception as e:
                session.rollback()
                raise e
        else:
            return narrative_event  # Return the narrative-event pair object without committing if using an external session

# Delete a Narrative-Event Pair
def delete_narrative_event(narrative_events_id, _session=None):
    session = _session or db.session
    narrative_event = session.get(NarrativeEvent, narrative_events_id)
    if narrative_event:
        session.delete(narrative_event)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return True  # Assume deletion is successful if using an external session

#Check a Narrative-Event Pair Existence
def get_narrative_events_id_by_narrative_and_event(primary_narrative_id, event_id, _session=None):
    session = _session or db.session
    # Query the narrative_events table for an entry matching the provided narrative ID and event ID
    narrative_event = session.query(NarrativeEvent).filter_by(narrative_id=primary_narrative_id, event_id=event_id).first()
    
    # If an entry exists, return its ID; otherwise return None
    return narrative_event.id if narrative_event else None


# Secondary Narrative Operations

# Create a Secondary Narrative
def create_secondary_narrative(original_narrative_id, updated_fact_combination_id, narrative_text, counterstrat_id, news, outcome_text, user_id, _session=None):
    session = _session or db.session
    new_secondary_narrative = SecondaryNarrative(
        original_narrative_id=original_narrative_id,
        updated_fact_combination_id=updated_fact_combination_id,
        narrative_text=narrative_text,
        counterstrat_id=counterstrat_id,
        news=news,
        outcome_text=outcome_text,
        user_id=user_id
    )
    session.add(new_secondary_narrative)
    db.session.commit()  
    if not _session:  # Commit only if not using an external session
        try:
            session.commit()
            return new_secondary_narrative
        except Exception as e:
            session.rollback()
            raise e
    else:
        return new_secondary_narrative  # Return the narrative object without committing if using an external session

# Read a Secondary Narrative
def get_secondary_narrative_by_id(secondary_narrative_id, _session=None):
    session = _session or db.session
    return session.get(SecondaryNarrative, secondary_narrative_id)

def get_all_secondary_narratives(_session=None):
    session = _session or db.session
    return session.execute(select(SecondaryNarrative)).scalars().all()

def get_secondary_narratives_by_original_narrative(original_narrative_id, _session=None):
    session = _session or db.session
    return session.execute(select(SecondaryNarrative).filter_by(original_narrative_id=original_narrative_id)).scalars().all()

def get_secondary_narrative_id_by_fact_combination_and_primary_narrative(primary_narrative_id, updated_fact_combination_id, _session=None):
    session = _session or db.session
    result = session.query(SecondaryNarrative.id).filter(
        SecondaryNarrative.original_narrative_id == primary_narrative_id,
        SecondaryNarrative.updated_fact_combination_id == updated_fact_combination_id
    ).first()
    return result.id if result else None


# Update a Secondary Narrative
def update_secondary_narrative(secondary_narrative_id, _session=None, **kwargs):
    session = _session or db.session
    secondary_narrative = session.get(SecondaryNarrative, secondary_narrative_id)
    if secondary_narrative:
        for key, value in kwargs.items():
            setattr(secondary_narrative, key, value)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return secondary_narrative
            except Exception as e:
                session.rollback()
                raise e
        else:
            return secondary_narrative  # Return the narrative object without committing if using an external session


# Delete a Secondary Narrative
def delete_secondary_narrative(secondary_narrative_id, _session=None):
    session = _session or db.session
    secondary_narrative = session.get(SecondaryNarrative, secondary_narrative_id)
    if secondary_narrative:
        session.delete(secondary_narrative)
        if not _session:  # Commit only if not using an external session
            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return True  # Assume deletion is successful if using an external session

# Get News Content by Secondary Narrative ID
def get_news_content_by_secondary_narrative_id(secondary_narrative_id, _session=None):
    session = _session or db.session
    result = session.query(SecondaryNarrative)\
        .filter(SecondaryNarrative.id == secondary_narrative_id)\
        .with_entities(SecondaryNarrative.resulting_headline, SecondaryNarrative.resulting_story, SecondaryNarrative.resulting_photo_url)\
        .first()

    if result:
        return {
            'headline': result.resulting_headline,
            'story': result.resulting_story,
            'photo_url': result.resulting_photo_url
        }
    else:
        return None




