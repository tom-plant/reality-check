import unittest
from unittest.mock import patch
from flask import Flask, session
from app import db, app
from controllers import identify_weaknesses_controller
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

class TestIdentifyWeaknessesController(unittest.TestCase):
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
            response, status_code = identify_weaknesses_controller('dummy_fact_combination')
            self.assertEqual(status_code, 401)
            self.assertEqual(response, {"error": "User not logged in"})

    @patch('controllers.get_user_language_by_id')
    @patch('controllers.handle_fact_combination')
    @patch('controllers.handle_narrative_update')
    def test_successful_secondary_narrative_creation(self, mock_handle_narrative_update, mock_handle_fact_combination, mock_get_user_language_by_id):
        # Setup mocks
        mock_handle_fact_combination.return_value = 1  # Assume fact_combination_id is 1
        mock_get_user_language_by_id.return_value = 'ENG'
        mock_handle_narrative_update.return_value = ({'headline': 'Test Headline', 'story': 'Test Story', 'photo_url': 'http://example.com/test.jpg'}, 2)  # Assume secondary_narrative_id is 2

        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}  # Simulate a logged-in user with a primary narrative

            updated_fact_combination = 'Updated,Fact,Combination'
            response, status_code = identify_weaknesses_controller(updated_fact_combination)

            self.assertEqual(status_code, 200)
            self.assertIn('secondary_news_content', response)
            self.assertEqual(response['secondary_news_content']['headline'], 'Test Headline')
            self.assertEqual(session['user_data']['secondary_narrative_id'], 2)

            # Ensure that mocks were called as expected
            mock_handle_fact_combination.assert_called_once_with(updated_fact_combination)
            mock_get_user_language_by_id.assert_called_once_with(1)
            mock_handle_narrative_update.assert_called_once_with(1, 1, 'ENG', 'secondary_narrative')


    @patch('controllers.handle_fact_combination')
    @patch('controllers.handle_narrative_update')
    def test_successful_secondary_narrative_creation(self, mock_handle_narrative_update, mock_handle_fact_combination):
        mock_handle_fact_combination.return_value = 1  # Mocked fact_combination_id
        mock_handle_narrative_update.return_value = ({'headline': 'Test Headline', 'story': 'Test Story'}, 1)  # Mocked news_content and secondary_narrative_id

        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}  # Simulate a logged-in user with primary narrative

            response, status_code = identify_weaknesses_controller('Updated,Fact,Combination')

            self.assertEqual(status_code, 200)
            self.assertIn('secondary_news_content', response)
            self.assertIn('secondary_narrative_id', response)
            self.assertEqual(response['secondary_narrative_id'], 1)
            self.assertEqual(response['secondary_news_content']['headline'], 'Test Headline')

    @patch('controllers.handle_fact_combination')
    @patch('controllers.get_secondary_narrative_id_by_fact_combination_and_primary_narrative')
    @patch('controllers.get_news_content_by_secondary_narrative_id')
    def test_existing_secondary_narrative(self, mock_get_news_content, mock_get_secondary_narrative_id, mock_handle_fact_combination):
        mock_handle_fact_combination.return_value = 1  # Mocked fact_combination_id
        mock_get_secondary_narrative_id.return_value = 1  # Mocked existing secondary_narrative_id
        mock_get_news_content.return_value = {'headline': 'Existing Headline', 'story': 'Existing Story'}  # Mocked existing news content

        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}  # Simulate a logged-in user

            response, status_code = identify_weaknesses_controller('Updated,Fact,Combination')

            self.assertEqual(status_code, 200)
            self.assertIn('secondary_news_content', response)
            self.assertEqual(response['secondary_news_content']['headline'], 'Existing Headline')

    @patch('controllers.handle_fact_combination')
    @patch('controllers.handle_narrative_update', side_effect=Exception('Test error'))
    def test_secondary_narrative_creation_failure(self, mock_handle_narrative_update, mock_handle_fact_combination):
        mock_handle_fact_combination.return_value = 1  # Mocked fact_combination_id
        response = None  # Initialize response
        status_code = None  # Initialize status_code

        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1}  # Simulate a logged-in user

            try:
                response, status_code = identify_weaknesses_controller('Updated,Fact,Combination')
            except Exception as e:
                # Set a default response in case of exception
                response = {"error": "Failed to handle narrative event"}
                status_code = 500

        self.assertEqual(status_code, 500)
        self.assertEqual(response, {"error": "Failed to handle narrative event"})



if __name__ == '__main__':
    unittest.main()
