import unittest
from unittest.mock import patch
from flask import Flask, session
from app import db
from controllers import select_narrative_controller  # Ensure this is the correct import path
from config import TestingConfig, FLASK_KEY

app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

class TestSelectNarrativeController(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.secret_key = FLASK_KEY
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    @patch('controllers.get_fact_combination_by_id') 
    @patch('controllers.initialize_data_controller')
    @patch('controllers.get_user_language_by_id')
    @patch('controllers.get_text')
    @patch('controllers.generate_news_content')
    def test_select_narrative_success(self, mock_generate_news, mock_get_text, mock_get_user_language, mock_initialize_data, mock_get_fact_combination):
        # Setup the mock for get_fact_combination_by_id to return a predefined fact combination
        mock_fact_combination = {'id': 'some_fact_combination_id', 'facts': ['fact1', 'fact2']}
        mock_get_fact_combination.return_value = mock_fact_combination
     
        # Mock the user language to be English
        mock_get_user_language.return_value = 'ENG'

        # Mock the get_text function to return specific prompts
        mock_get_text.side_effect = lambda language_code, key, selected_facts: f"Mocked {key} in {language_code} with facts {selected_facts}"

        # Mock the news content generation to return a predefined news data
        mock_news_data = {'headline': 'Mocked Headline', 'story': 'Mocked Story', 'photo_url': 'mocked_url.jpg'}
        mock_generate_news.return_value = mock_news_data

        # Simulate the user session
        with app.test_request_context():
            session['user_data'] = {'user_id': '1', 'fact_combination_id': 'some_fact_combination_id'}

            # Call the controller function with a mocked narrative
            response = select_narrative_controller('selected_narrative')

            self.assertEqual(response, {"news_data": mock_news_data})
            mock_initialize_data.assert_not_called()  # Check that the initialize_data_controller was not called

            # Verify get_fact_combination_by_id was called with the correct fact_combination_id
            mock_get_fact_combination.assert_called_once_with('some_fact_combination_id')

    @patch('controllers.get_user_language_by_id')
    def test_user_not_logged_in(self, mock_get_user_language):
        mock_get_user_language.return_value = 'ENG'

        with app.test_request_context():
            # Clear session at the beginning of the test
            with self.app as client:
                with client.session_transaction() as sess:
                    sess.clear()

                response = select_narrative_controller('selected_narrative')
                self.assertEqual(response, ({"error": "User not logged in"}, 401))  

if __name__ == '__main__':
    unittest.main()
