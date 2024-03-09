import unittest
from unittest.mock import patch
from flask import Flask
from app import db
from controllers import select_facts_controller
from config import TestingConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

class TestSelectFactsController(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.request_context = app.test_request_context()
        self.request_context.push()  # Simulate a request context for your tests

        # Simulate a logged-in user by initializing 'user_data' in session
        with self.request_context:
            from flask import session
            session['user_data'] = {
                'user_id': 1,  # Assuming 1 is a valid user_id for testing purposes
                'fact_combination_id': None,
                'primary_narrative_id': None,
                'secondary_narrative_id': None,
                'narrative_events_id': None,
            }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if self.request_context:
            self.request_context.pop()
        self.app_context.pop()

    @patch('controllers.generate_additional_narratives')
    @patch('controllers.get_narratives_by_fact_combination')
    def test_returns_three_narratives_if_matched(self, mock_generate, mock_get_narratives):
        # Ensure generate_additional_narratives does not get called, but set a return value in case it does
        mock_generate.return_value = []
        # Set up the mock to return a list of narratives
        mock_get_narratives.return_value = ['Narrative 1', 'Narrative 2', 'Narrative 3']

        selected_facts = [1, 2]
        expected_narratives = {"narratives": ['Narrative 1', 'Narrative 2', 'Narrative 3']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)

    @patch('controllers.get_narratives_by_fact_combination')
    @patch('controllers.generate_additional_narratives')
    def test_returns_three_narratives_when_two_are_found(self, mock_get_narratives, mock_generate):
        mock_get_narratives.return_value = ['Narrative 1', 'Narrative 2']
        mock_generate.return_value = ['Generated Narrative 1']

        selected_facts = [1, 2]
        expected_narratives = {"narratives": ['Generated Narrative 1', 'Narrative 1', 'Narrative 2']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)

    @patch('controllers.generate_additional_narratives')
    @patch('controllers.get_narratives_by_fact_combination')
    def test_returns_three_narratives_when_one_is_found(self, mock_get_narratives, mock_generate):
        mock_get_narratives.return_value = ['Narrative 1']
        mock_generate.return_value = ['Generated Narrative 1', 'Generated Narrative 2']
        
        selected_facts = [3]

        actual_response = select_facts_controller(selected_facts)
        
        expected_narratives = {"narratives": ['Narrative 1', 'Generated Narrative 1', 'Generated Narrative 2']}
        self.assertEqual(actual_response, expected_narratives)

    @patch('controllers.get_narratives_by_fact_combination')
    @patch('controllers.generate_additional_narratives')
    def test_returns_three_generated_narratives_when_none_are_found(self, mock_get_narratives, mock_generate):
        mock_get_narratives.return_value = []
        mock_generate.return_value = ['Generated Narrative 1', 'Generated Narrative 2', 'Generated Narrative 3']

        selected_facts = [4, 5]
        expected_narratives = {"narratives": ['Generated Narrative 1', 'Generated Narrative 2', 'Generated Narrative 3']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)

if __name__ == '__main__':
    unittest.main()