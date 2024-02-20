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

def create_primary_narrative(narrative, headline, news_story, photo, user_id):
    new_narrative = PrimaryNarrative(narrative=narrative, headline=headline, news_story=news_story, photo=photo, user_id=user_id)
    db.session.add(new_narrative)
    db.session.commit()

def get_primary_narrative_by_id(narrative_id):
    return PrimaryNarrative.query.get(narrative_id)

def update_primary_narrative(narrative_id, new_narrative, new_headline, new_news_story, new_photo):
    narrative = PrimaryNarrative.query.get(narrative_id)
    narrative.narrative = new_narrative
    narrative.headline = new_headline
    narrative.news_story = new_news_story
    narrative.photo = new_photo
    db.session.commit()
 
def delete_primary_narrative(narrative_id):
    narrative = PrimaryNarrative.query.get(narrative_id)
    db.session.delete(narrative)
    db.session.commit()


# Secondary Narrative Operations

def create_secondary_narrative(parent_narrative_id, event_id, narrative, outcome):
    new_secondary_narrative = SecondaryNarrative(parent_narrative_id=parent_narrative_id, event_id=event_id, narrative=narrative, outcome=outcome)
    db.session.add(new_secondary_narrative)
    db.session.commit()

def get_secondary_narrative_by_id(narrative_id):
    return SecondaryNarrative.query.get(narrative_id)

def update_secondary_narrative(narrative_id, parent_narrative_id, event_id, narrative, outcome):
    secondary_narrative = SecondaryNarrative.query.get(narrative_id)
    if secondary_narrative:
        secondary_narrative.parent_narrative_id = parent_narrative_id
        secondary_narrative.event_id = event_id
        secondary_narrative.narrative = narrative
        secondary_narrative.outcome = outcome
        db.session.commit()

def delete_secondary_narrative(narrative_id):
    secondary_narrative = SecondaryNarrative.query.get(narrative_id)
    if secondary_narrative:
        db.session.delete(secondary_narrative)
        db.session.commit()


# Facts Operations

def get_facts_by_language(language):
    return Fact.query.filter_by(language=language).all()


# Events Operations for events filtered by language

def get_events_by_language(language):
    return Event.query.filter_by(language=language).all()


# NarrativeFactAssociation Operations
# Read narratives associated with a given set of facts

def get_narratives_by_facts(fact_ids):
    return db.session.query(PrimaryNarrative).\
        filter(PrimaryNarrative.id == NarrativeFactAssociation.narrative_id).\
        filter(NarrativeFactAssociation.fact_id.in_(fact_ids)).\
        all()


# # Function to update the association between a narrative and selected facts
# def update_narrative_association(narrative_id, selected_facts):
#     # Check if associations already exist for the given narrative
#     existing_associations = NarrativeFactAssociation.query.filter_by(narrative_id=narrative_id).all()

#     # Retrieve existing fact IDs
#     existing_fact_ids = [association.fact_id for association in existing_associations]

#     # Create new associations for the given narrative and selected facts
#     for fact_id in selected_facts:
#         # Only create associations for facts that are not already associated with the narrative
#         if fact_id not in existing_fact_ids:
#             association = NarrativeFactAssociation(narrative_id=narrative_id, fact_id=fact_id)
#             db.session.add(association)

#     # Commit changes to the database
#     db.session.commit()