import unittest
from unittest.mock import patch
from flask import Flask, session
from app import db
from controllers import introduce_event_controller
from config import TestingConfig
from localization import get_text

app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

class TestIntroduceEventController(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.request_context = app.test_request_context()
        self.request_context.push()  # Simulate a request context for your tests

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
    def test_no_event_found(self, mock_get_random_event):
        with app.test_request_context():
            session['user_data'] = {'user_id': 1}
            mock_get_random_event.return_value = None
            response = introduce_event_controller()
            self.assertEqual(response, ({"error": "No event found"}, 404))

    @patch('controllers.get_random_event')
    @patch('controllers.get_primary_narrative_by_id')
    def test_selected_narrative_not_found(self, mock_get_primary_narrative_by_id, mock_get_random_event):
        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1, 'fact_combination_id': 4}
            mock_get_random_event.return_value = "Event"
            mock_get_primary_narrative_by_id.return_value = None
            response = introduce_event_controller()
            self.assertEqual(response, ({"error": "Selected narrative not found"}, 404))

    @patch('controllers.get_random_event')
    @patch('controllers.get_primary_narrative_by_id')
    @patch('controllers.handle_event_selection')
    @patch('controllers.generate_and_store_news_content')
    def test_news_content_generation_success(self, mock_generate_and_store, mock_handle_event, mock_get_primary_narrative, mock_get_random_event):
        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1, 'fact_combination_id': 1}
            mock_get_random_event.return_value = "Event"
            mock_get_primary_narrative.return_value = "Narrative"
            mock_handle_event.return_value = ("narrative_event", True)
            mock_generate_and_store.return_value = {"headline": "Headline", "story": "Story"}
            response = introduce_event_controller()
            self.assertEqual(response, ({"event_news_content": {"headline": "Headline", "story": "Story"}}, 200))

    @patch('controllers.get_random_event')
    @patch('controllers.get_primary_narrative_by_id')
    @patch('controllers.handle_event_selection')
    @patch('controllers.generate_and_store_news_content')
    def test_news_content_generation_failure(self, mock_generate_and_store, mock_handle_event, mock_get_primary_narrative, mock_get_random_event):
        with app.test_request_context():
            session['user_data'] = {'user_id': 1, 'primary_narrative_id': 1, 'fact_combination_id': 1}
            mock_get_random_event.return_value = "Event"
            mock_get_primary_narrative.return_value = "Narrative"
            mock_handle_event.return_value = ("narrative_event", True)
            mock_generate_and_store.return_value = None
            response = introduce_event_controller()
            self.assertEqual(response, ({"error": "Failed to generate news content"}, 500))

if __name__ == '__main__':
    unittest.main()


