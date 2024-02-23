# db_operations.py

from app import db
from models import User, PrimaryNarrative, SecondaryNarrative, Fact, Event, NarrativeFactAssociation


# # User Operations

# def create_user(username, password):
#     new_user = User(username=username, password=password)
#     db.session.add(new_user)
#     db.session.commit()

# def get_user_by_id(user_id):
#     return User.query.get(user_id)

# def delete_user(user_id):
#     user = User.query.get(user_id)
#     db.session.delete(user)
#     db.session.commit()


# Primary Narrative Operations

def create_primary_narrative(narrative, headline, news_story, photo, user_id, _session=None):
    session = _session or db.session
    new_narrative = PrimaryNarrative(narrative=narrative, headline=headline, news_story=news_story, photo=photo, user_id=user_id)
    session.add(new_narrative)
    session.commit()


def get_primary_narrative_by_id(narrative_id, _session=None):
    session = _session or db.session
    return session.get(PrimaryNarrative, narrative_id)


def update_primary_narrative(narrative_id, new_narrative, new_headline, new_news_story, new_photo, _session=None):
    session = _session or db.session
    narrative = session.get(PrimaryNarrative, narrative_id)
    narrative.narrative = new_narrative
    narrative.headline = new_headline
    narrative.news_story = new_news_story
    narrative.photo = new_photo
    session.commit()
 
def delete_primary_narrative(narrative_id, _session=None):
    session = _session or db.session
    # Delete any associated NarrativeFactAssociation records
    associations = session.query(NarrativeFactAssociation).filter_by(narrative_id=narrative_id).all()
    for association in associations:
        session.delete(association)
    session.flush()  # Flush changes to ensure associations are deleted

    # Delete the PrimaryNarrative
    narrative = session.get(PrimaryNarrative, narrative_id)
    if narrative:
        session.delete(narrative)
        session.commit()

# Secondary Narrative Operations

def create_secondary_narrative(parent_narrative_id, event_id, narrative, outcome, _session=None):
    session = _session or db.session
    new_secondary_narrative = SecondaryNarrative(parent_narrative_id=parent_narrative_id, event_id=event_id, narrative=narrative, outcome=outcome)
    session.add(new_secondary_narrative)
    session.flush()  # Ensure the object is persisted within the transaction

def get_secondary_narrative_by_id(narrative_id, _session=None):
    session = _session or db.session
    return session.get(SecondaryNarrative, narrative_id)

def update_secondary_narrative(narrative_id, parent_narrative_id, event_id, narrative, outcome, _session=None):
    session = _session or db.session
    secondary_narrative = session.get(SecondaryNarrative, narrative_id)
    if secondary_narrative:
        secondary_narrative.parent_narrative_id = parent_narrative_id
        secondary_narrative.event_id = event_id
        secondary_narrative.narrative = narrative
        secondary_narrative.outcome = outcome
        session.commit()

def delete_secondary_narrative(narrative_id, _session=None):
    session = _session or db.session
    secondary_narrative = session.get(SecondaryNarrative, narrative_id)
    if secondary_narrative:
        session.delete(secondary_narrative)
        session.commit()


# Facts Operations

def get_facts_by_language(language, _session=None):
    session = _session or db.session
    return session.query(Fact).filter_by(language=language).all()


# Events Operations for events filtered by language

def get_events_by_language(language, _session=None):
    session = _session or db.session
    return session.query(Event).filter_by(language=language).all()


# NarrativeFactAssociation Operations
# Read narratives associated with a given set of facts

def get_narratives_by_facts(fact_ids, _session=None):
    session = _session or db.session
    result = session.query(PrimaryNarrative)\
        .join(NarrativeFactAssociation, PrimaryNarrative.id == NarrativeFactAssociation.narrative_id)\
        .filter(NarrativeFactAssociation.fact_id.in_(fact_ids))\
        .all()

    return result if result is not None else []

# Function to update the association between a narrative and selected facts
def update_narrative_association(narrative_id, selected_facts, _session=None):
    session = _session or db.session

    # First, check for existing associations for this narrative
    existing_associations = session.query(NarrativeFactAssociation).filter_by(narrative_id=narrative_id).all()
    existing_fact_ids = [assoc.fact_id for assoc in existing_associations]

    # Add new associations for facts not already associated with this narrative
    for fact_id in selected_facts:
        if fact_id not in existing_fact_ids:
            new_association = NarrativeFactAssociation(narrative_id=narrative_id, fact_id=fact_id)
            session.add(new_association)

    session.commit()  # Commit at the end to persist all new associations