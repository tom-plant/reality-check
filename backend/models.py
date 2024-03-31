#models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Define models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Fact(db.Model):
    __tablename__ = 'facts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)  # Assuming text includes language-specific representation
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)  # Assuming text includes language-specific representation
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)

class FactCombination(db.Model):
    __tablename__ = 'fact_combinations'

    id = db.Column(db.Integer, primary_key=True)
    facts = db.Column(db.String(1000), nullable=False)  # This could be a JSON string or a delimited list of fact texts
    primary_narratives = db.relationship('PrimaryNarrative', backref='fact_combination', lazy=True, cascade="all, delete-orphan")
    secondary_narratives = db.relationship('SecondaryNarrative', backref='updated_fact_combination', lazy=True)  # Add this line

class PrimaryNarrative(db.Model):
    __tablename__ = 'primary_narratives'

    id = db.Column(db.Integer, primary_key=True)
    fact_combination_id = db.Column(db.Integer, db.ForeignKey('fact_combinations.id'), nullable=False)
    narrative_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    headline = db.Column(db.String(1000), nullable=False)
    story = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(1000), nullable=True)  # Assuming URLs are stored for photos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    narrative_events = db.relationship('NarrativeEvent', backref='primary_narrative', lazy=True, cascade="all, delete-orphan")
    secondary_narratives = db.relationship('SecondaryNarrative', backref='original_narrative', lazy=True, cascade="all, delete-orphan")

class NarrativeEvent(db.Model):
    __tablename__ = 'narrative_events'

    id = db.Column(db.Integer, primary_key=True)
    narrative_id = db.Column(db.Integer, db.ForeignKey('primary_narratives.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    resulting_headline = db.Column(db.String(1000), nullable=False)
    resulting_story = db.Column(db.Text, nullable=False)
    resulting_photo_url = db.Column(db.String(1000), nullable=True)

class SecondaryNarrative(db.Model):
    __tablename__ = 'secondary_narratives'

    id = db.Column(db.Integer, primary_key=True)
    original_narrative_id = db.Column(db.Integer, db.ForeignKey('primary_narratives.id'), nullable=False)
    updated_fact_combination_id = db.Column(db.Integer, db.ForeignKey('fact_combinations.id'), nullable=False)  
    narrative_text = db.Column(db.Text, nullable=False) 
    resulting_headline = db.Column(db.String(1000), nullable=False)
    resulting_story = db.Column(db.Text, nullable=False)
    resulting_photo_url = db.Column(db.String(1000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
