import unittest
from flask import Flask, session
from app import db, app
from controllers import select_narrative_controller  
from config import TestingConfig
from unittest.mock import patch
from models import FactCombination, User
from dotenv import load_dotenv
import os


load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
app.config.from_object(TestingConfig)

class TestGenerateNewsContent(unittest.TestCase):

    def setUp(self):
        global app  
        self.app_context = app.app_context()
        self.app_context.push()
        app.config.from_object('config.TestingConfig')  # Make sure TestingConfig is used
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI')
        db.create_all()
        self.request_context = app.test_request_context()
        self.request_context.push()

        # Create and commit a FactCombination instance to the database
        test_fact_combination = FactCombination(id=8, facts="border wall incomplete, migrant crime term coined by Trump")
        db.session.add(test_fact_combination)
        db.session.commit()  

        # Create and commit a test user to the database
        test_user = User(id=1, username="testuser", email="testuser@example.com", language='ENG')  # Adjust the fields based on your User model
        db.session.add(test_user)
        db.session.commit()  

        # Manually set up session data needed for the test
        session['user_data'] = {
            'user_id': test_user.id,
            'fact_combination_id': 8,  # Make sure this matches your actual data structure
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
        self.assertIn('news_content', result)
        

if __name__ == '__main__':
    unittest.main()
