#models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
if os.getenv('FLASK_ENV') == 'production':
    from backend.app import db
else:
    from app import db

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
    text = db.Column(db.String(1000), nullable=False) 
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False) 
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)  
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)

class Strat(db.Model):
    __tablename__ = 'strats'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False) 
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)

class CounterStrat(db.Model):
    __tablename__ = 'counterstrats'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False) 
    language = db.Column(db.Enum('ENG', 'EST', 'RUS', name='language_types'), default='ENG', nullable=False)

class StrategyEffectiveness(db.Model):
    __tablename__ = 'strategy_effectiveness'

    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strats.id'), nullable=False)
    counter_strategy_id = db.Column(db.Integer, db.ForeignKey('counterstrats.id'), nullable=False)
    effectiveness = db.Column(db.Enum('weak', 'medium', 'strong', name='effectiveness_types'), default='medium', nullable=False)

    strategy = db.relationship('Strat', foreign_keys=[strategy_id], backref='effectiveness_as_strategy')
    counter_strategy = db.relationship('CounterStrat', foreign_keys=[counter_strategy_id], backref='effectiveness_as_counter_strategy')

class FactCombination(db.Model):
    __tablename__ = 'fact_combinations'

    id = db.Column(db.Integer, primary_key=True)
    facts = db.Column(db.String(1000), nullable=False)  
    primary_narratives = db.relationship('PrimaryNarrative', backref='fact_combination', lazy=True, cascade="all, delete-orphan")
    secondary_narratives = db.relationship('SecondaryNarrative', backref='updated_fact_combination', lazy=True)  

class PrimaryNarrative(db.Model):
    __tablename__ = 'primary_narratives'

    id = db.Column(db.Integer, primary_key=True)
    fact_combination_id = db.Column(db.Integer, db.ForeignKey('fact_combinations.id'), nullable=False)
    narrative_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    strat_id = db.Column(db.Integer, db.ForeignKey('strats.id'), nullable=False)
    news = db.Column(db.JSON, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    narrative_events = db.relationship('NarrativeEvent', backref='primary_narrative', lazy=True, cascade="all, delete-orphan")
    secondary_narratives = db.relationship('SecondaryNarrative', backref='original_narrative', lazy=True, cascade="all, delete-orphan")

class NarrativeEvent(db.Model):
    __tablename__ = 'narrative_events'

    id = db.Column(db.Integer, primary_key=True)
    narrative_id = db.Column(db.Integer, db.ForeignKey('primary_narratives.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event_outcome_text = db.Column(db.Text, nullable=False) 

class SecondaryNarrative(db.Model):
    __tablename__ = 'secondary_narratives'

    id = db.Column(db.Integer, primary_key=True)
    original_narrative_id = db.Column(db.Integer, db.ForeignKey('primary_narratives.id'), nullable=False)
    updated_fact_combination_id = db.Column(db.Integer, db.ForeignKey('fact_combinations.id'), nullable=False)  
    narrative_text = db.Column(db.Text, nullable=False) 
    counterstrat_id = db.Column(db.Integer, db.ForeignKey('counterstrats.id'), nullable=False)
    news = db.Column(db.JSON, nullable=False)  
    outcome_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)