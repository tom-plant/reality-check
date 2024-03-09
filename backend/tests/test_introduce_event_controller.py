import unittest
from unittest.mock import patch
from flask import Flask, session
from app import db, app
from controllers import introduce_event_controller
from config import TestingConfig
from datetime import datetime
from models import PrimaryNarrative, FactCombination, User, Event
import logging
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
app.config.from_object(TestingConfig)

class MockEvent:
    def __init__(self, event_id, text="Some event text", language="ENG"):
        self.id = event_id
        self.text = text
        self.language = language

class MockPrimaryNarrative:
    def __init__(self, id=1, fact_combination_id=1, narrative_text="Some narrative text", user_id=1, headline="Some headline", story="Some story", photo_url=None, created_at=None):
        self.id = id
        self.fact_combination_id = fact_combination_id
        self.narrative_text = narrative_text
        self.user_id = user_id
        self.headline = headline
        self.story = story
        self.photo_url = photo_url
        self.created_at = created_at or datetime.utcnow()
        self.narrative_events = []
        self.secondary_narratives = []

class TestIntroduceEventController(unittest.TestCase):
    def setUp(self):
        global app  
        app.config.from_object('config.TestingConfig')  # Make sure TestingConfig is used
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI')
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.request_context = app.test_request_context()
        self.request_context.push()

        # Create a mock user
        mock_user = User(username="testuser", email="testuser@example.com", language="ENG")
        db.session.add(mock_user)
        db.session.flush()  # Flush to assign an ID to mock_user without committing the transaction

        # Create FactCombination entry
        fact_combination = FactCombination(facts="Some facts")
        db.session.add(fact_combination)
        db.session.flush()  # Flush to assign an ID to fact_combination without committing the transaction

        # Create a mock event
        mock_event = Event(text="Some event text", language="ENG")
        db.session.add(mock_event)
        db.session.flush()  # Flush to assign an ID to mock_event without committing the transaction

        # Use fact_combination.id for the fact_combination_id field and mock_user.id for the user_id field in PrimaryNarrative
        primary_narrative = PrimaryNarrative(fact_combination_id=fact_combination.id, narrative_text="Some narrative text", user_id=mock_user.id, headline="Some headline", story="Some story")
        db.session.add(primary_narrative)
        db.session.commit()
        self.primary_narrative_id = primary_narrative.id


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if self.request_context:
            self.request_context.pop()
        self.app_context.pop()

    def test_user_not_logged_in(self):
        with app.test_request_context():
            response = introduce_event_controller()
            self.assertEqual(response, ({"error": "User not logged in"}, 401))

    @patch('controllers.get_random_event')
    @patch('controllers.get_user_language_by_id', return_value='ENG')  
    def test_no_event_found(self, mock_get_language, mock_get_random_event):
        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}  
            mock_get_random_event.return_value = None  
            response = introduce_event_controller()
            self.assertEqual(response, ({"error": "No event found"}, 404))

    @patch('controllers.get_random_event')
    @patch('controllers.get_primary_narrative_by_id')
    def test_selected_narrative_not_found(self, mock_get_primary_narrative_by_id, mock_get_random_event):
        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}
            mock_get_random_event.return_value = MockEvent(1)
            mock_get_primary_narrative_by_id.return_value = None
            response = introduce_event_controller()
            self.assertEqual(response, ({"error": "Selected narrative not found"}, 404))

    @patch('controllers.get_random_event')
    @patch('controllers.get_primary_narrative_by_id')
    @patch('controllers.generate_event_news_content')
    def test_news_content_generation_success(self, mock_generate_event_news_content, mock_get_primary_narrative_by_id, mock_get_random_event):
        with app.test_request_context():
            mock_get_random_event.return_value = MockEvent(1)
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}
            mock_get_primary_narrative_by_id.return_value = 'Narrative'
            mock_generate_event_news_content.return_value = {"headline": "Headline", "story": "Story", "image_url": "Image URL"}
            response = introduce_event_controller()
            self.assertEqual(response, ({"event_news_content": {"headline": "Headline", "story": "Story", "image_url": "Image URL"}, "narrative_event_id": None}, 200))

    @patch('controllers.get_random_event')
    @patch('controllers.get_primary_narrative_by_id')
    @patch('controllers.generate_event_news_content', return_value=None)
    def test_news_content_generation_failure(self, mock_generate_event_news_content, mock_get_primary_narrative_by_id, mock_get_random_event):
        with app.test_request_context():
            mock_get_random_event.return_value = MockEvent(1)
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}
            mock_get_primary_narrative_by_id.return_value = 'Narrative'
            mock_generate_event_news_content.return_value = None
            response = introduce_event_controller()
            self.assertEqual(response, ({"error": "Failed to handle narrative event"}, 500))

if __name__ == '__main__':
    unittest.main()
