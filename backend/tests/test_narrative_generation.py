#test_narrative_generation.py

import unittest
from controllers import generate_additional_narratives 

class TestChatGPTAPIIntegration(unittest.TestCase):

    def test_no_pre_generated_narratives(self):
        # Scenario with 0 pre-generated narratives, requiring 3 narratives to be generated
        selected_facts = ['Economic downturn', 'Technological breakthrough', 'Political election']
        num_additional_narratives = 3  # Need to generate 3 narratives

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), num_additional_narratives)
        for narrative in narratives:
            self.assertIsInstance(narrative, str)

    def test_one_pre_generated_narrative(self):
        # Scenario with 1 pre-generated narrative, requiring 2 more narratives to be generated
        selected_facts = ['Economic downturn', 'Technological breakthrough', 'Political election']
        num_additional_narratives = 2  # Need to generate 2 more narratives

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), num_additional_narratives)
        for narrative in narratives:
            self.assertIsInstance(narrative, str)

    def test_two_pre_generated_narratives(self):
        # Scenario with 2 pre-generated narratives, requiring 1 more narrative to be generated
        selected_facts = ['Economic downturn', 'Technological breakthrough', 'Political election']
        num_additional_narratives = 1  # Need to generate 1 more narrative

        narratives = generate_additional_narratives(selected_facts, num_additional_narratives)

        self.assertIsInstance(narratives, list)
        self.assertEqual(len(narratives), num_additional_narratives)
        for narrative in narratives:
            self.assertIsInstance(narrative, str)

if __name__ == '__main__':
    unittest.main()