from flask_sqlalchemy import SQLAlchemy
from app import db

# Assuming you've already initialized Flask app and configured SQLAlchemy

# Define the SQLAlchemy instance
db = SQLAlchemy(app)

# Define models
class PrimaryNarrative(db.Model):
    __tablename__ = 'primary_narratives'

    id = db.Column(db.Integer, primary_key=True)
    narrative = db.Column(db.Text, nullable=False)
    headline = db.Column(db.Text, nullable=False)
    news_story = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class SecondaryNarrative(db.Model):
    __tablename__ = 'secondary_narratives'

    id = db.Column(db.Integer, primary_key=True)
    parent_narrative_id = db.Column(db.Integer, db.ForeignKey('primary_narratives.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    narrative = db.Column(db.Text, nullable=False)
    outcome = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Fact(db.Model):
    __tablename__ = 'facts'

    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    is_key_fact = db.Column(db.Boolean, nullable=False)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)

class NarrativeFactAssociation(db.Model):
    __tablename__ = 'narrative_fact_associations'

    narrative_id = db.Column(db.Integer, db.ForeignKey('primary_narratives.id'), primary_key=True)
    fact_id = db.Column(db.Integer, db.ForeignKey('facts.id'), primary_key=True)

# Run this command to create the tables in the MySQL database
db.create_all()


