import unittest
from flask import Flask, session
from app import db
from controllers import select_narrative_controller  
from config import TestingConfig
from unittest.mock import patch

app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

class TestGenerateNewsContent(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.request_context = app.test_request_context()
        self.request_context.push()
        # Manually set up session data needed for the test
        session['user_data'] = {
            'user_id': '1',
            'fact_combination_id': 'some_fact_id',  # Make sure this matches your actual data structure
            # Add other 'user_data' fields as needed
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if self.request_context:
            self.request_context.pop()
        self.app_context.pop()

    @patch('controllers.get_user_language_by_id')
    @patch('controllers.get_fact_combination_by_id')
    def test_select_narrative_controller_integration(self, mock_get_fact_combination_by_id, mock_get_user_language):
        mock_get_user_language.return_value = 'ENG'  # Mock the language code
        mock_get_fact_combination_by_id.return_value = ["border wall incomplete", "migrant crime term coined by Trump"]  # Mock the selected facts
        selected_narrative = "Building the border wall is absolutely necessary for the defense of our nation due to rising migrant crime and overflows at our border."

        # Call the select_narrative_controller function directly
        result = select_narrative_controller(selected_narrative)
        print(result)

        # Assert that the result contains 'news_data'
        self.assertIn('news_data', result)
        
        # Further assertions can be added to test the content of 'news_data' based on expected outcomes

if __name__ == '__main__':
    unittest.main()
