#test_select_facts_controller.py

import sys
import os
sys.path.append(os.path.abspath('..'))

import unittest
from unittest.mock import patch
from controllers import select_facts_controller 

class TestSelectFactsController(unittest.TestCase):

    @patch('controllers.get_narratives_by_facts')  
    @patch('controllers.generate_additional_narratives')  
    def test_returns_three_narratives_if_matched(self, mock_generate, mock_get_narratives):
        mock_get_narratives.return_value = ['Narrative 1', 'Narrative 2', 'Narrative 3']
        selected_facts = ['Fact 1', 'Fact 2']
        expected_narratives = {"narratives": ['Narrative 1', 'Narrative 2', 'Narrative 3']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)
        self.assertIsInstance(actual_response['narratives'], list)
        self.assertEqual(len(actual_response['narratives']), 3)

    @patch('controllers.generate_additional_narratives')
    @patch('controllers.get_narratives_by_facts')
    def test_returns_three_narratives_when_two_are_found(self, mock_get_narratives, mock_generate):
        mock_get_narratives.return_value = ['Narrative 1', 'Narrative 2']
        mock_generate.return_value = ['Generated Narrative 1']
        selected_facts = ['Fact 1', 'Fact 2']
        expected_narratives = {"narratives": ['Narrative 1', 'Narrative 2', 'Generated Narrative 1']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)
        self.assertIsInstance(actual_response['narratives'], list)
        self.assertEqual(len(actual_response['narratives']), 3)

    @patch('controllers.generate_additional_narratives')
    @patch('controllers.get_narratives_by_facts')
    def test_returns_three_narratives_when_one_is_found(self, mock_get_narratives, mock_generate):
        mock_get_narratives.return_value = ['Narrative 1']
        mock_generate.return_value = ['Generated Narrative 1', 'Generated Narrative 2']
        selected_facts = ['Fact 3']
        expected_narratives = {"narratives": ['Narrative 1', 'Generated Narrative 1', 'Generated Narrative 2']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)
        self.assertIsInstance(actual_response['narratives'], list)
        self.assertEqual(len(actual_response['narratives']), 3)

    @patch('controllers.generate_additional_narratives')
    @patch('controllers.get_narratives_by_facts')
    def test_returns_three_generated_narratives_when_none_are_found(self, mock_get_narratives, mock_generate):
        mock_get_narratives.return_value = []
        mock_generate.return_value = ['Generated Narrative 1', 'Generated Narrative 2', 'Generated Narrative 3']
        selected_facts = ['Fact 4', 'Fact 5']
        expected_narratives = {"narratives": ['Generated Narrative 1', 'Generated Narrative 2', 'Generated Narrative 3']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)
        self.assertIsInstance(actual_response['narratives'], list)
        self.assertEqual(len(actual_response['narratives']), 3)

    @patch('controllers.generate_additional_narratives')
    @patch('controllers.get_narratives_by_facts')
    def test_returns_generated_narratives_if_none_matched(self, mock_generate, mock_get_narratives):
        mock_get_narratives.return_value = []
        mock_generate.return_value = ['Generated Narrative 1', 'Generated Narrative 2', 'Generated Narrative 3']
        selected_facts = ['Fact 5']
        expected_narratives = {"narratives": ['Generated Narrative 1', 'Generated Narrative 2', 'Generated Narrative 3']}

        actual_response = select_facts_controller(selected_facts)

        self.assertEqual(actual_response, expected_narratives)
        self.assertIsInstance(actual_response['narratives'], list)
        self.assertEqual(len(actual_response['narratives']), 3)

    # Add more tests for other edge cases as needed

if __name__ == '__main__':
    unittest.main()
