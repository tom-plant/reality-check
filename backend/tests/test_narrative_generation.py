import unittest
from unittest.mock import patch
from flask import Flask, session
from app import db  
from controllers import generate_additional_narratives
from localization import get_text
from config import TestingConfig  # Ensure this is your actual testing configuration

app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

class TestGenerateAdditionalNarratives(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()  # Activate the app context
        db.create_all()  # Create database schema for tests
        self.request_context = app.test_request_context()
        self.request_context.push()  # Simulate a request context for your tests
        # Manually set up session data needed for the test
        session['user_data'] = {
            'user_id': '1',
            # Other 'user_data' fields as needed
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if self.request_context:
            self.request_context.pop()  # Pop the request context to clean up after tests
        self.app_context.pop()  # Pop the app context to clean up after tests


    @patch('controllers.get_user_language_by_id')
    def test_no_pre_generated_narratives(self, mock_language):
        
        # Scenario with 0 pre-generated narratives, requiring 3 narratives to be generated
        mock_language.return_value = 'ENG'  # Defaulting to English for this test
        selected_facts = ['Economic downturn', 'Technological breakthrough', 'Political election']
        num_additional_narratives = 3  # Need to generate 3 narratives

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), (num_additional_narratives))
        for narrative in narratives:
            self.assertIsInstance(narrative, str)

    @patch('controllers.get_user_language_by_id')
    def test_one_pre_generated_narrative(self, mock_language):
        # Scenario with 1 pre-generated narrative, requiring 2 more narratives to be generated
        mock_language.return_value = 'ENG'  # Defaulting to English for this test
        selected_facts = ['Explosion near Pentagon', 'Israel-Gaza War', 'Self-immolation']
        pre_generated_narratives = ['narrative1']
        num_additional_narratives = 3 - len(pre_generated_narratives)  # Need to generate 2 more narratives

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), (num_additional_narratives))
        for narrative in narratives:
            self.assertIsInstance(narrative, str)

    @patch('controllers.get_user_language_by_id')
    def test_two_pre_generated_narratives(self, mock_language):
        # Scenario with 2 pre-generated narratives, requiring 1 more narrative to be generated
        mock_language.return_value = 'ENG'  # Defaulting to English for this test
        selected_facts = ['Power outage during contentious election', 'Far right leader claims sabatoge', 'Centrist leader blames foreign intervention']
        pre_generated_narratives = ['narrative1', 'narrative2']
        num_additional_narratives = 3 - len(pre_generated_narratives)  # Need to generate 1 more narratives

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), num_additional_narratives)
        for narrative in narratives:
            self.assertIsInstance(narrative, str)

    # The rest of the language-specific tests follow here
    # English
    @patch('controllers.get_user_language_by_id')
    def test_generate_narratives_english(self, mock_language):
        mock_language.return_value = 'ENG'
        selected_facts = ['power grid attacked', 'super computer compromised in China', 'Russian prisoner killed']
        num_additional_narratives = 1

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), num_additional_narratives)
       
    # Estonian
    @patch('controllers.get_user_language_by_id')
    def test_generate_narratives_estonian(self, mock_language):
        mock_language.return_value = 'EST'
        selected_facts = ['power grid attacked', 'super computer compromised in China', 'Russian prisoner killed']
        num_additional_narratives = 1

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), num_additional_narratives)


    # Russian
    @patch('controllers.get_user_language_by_id')
    def test_generate_narratives_russian(self, mock_language):
        mock_language.return_value = 'RUS'
        selected_facts = ['power grid attacked', 'super computer compromised in China', 'Russian prisoner killed']
        num_additional_narratives = 1

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), num_additional_narratives)

if __name__ == '__main__':
    unittest.main()
