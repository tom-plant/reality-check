import unittest
from flask import Flask, session
from app import db
from controllers import generate_news_content  
from localization import get_text
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
            # Other 'user_data' fields as needed
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if self.request_context:
            self.request_context.pop()
        self.app_context.pop()

    @patch('controllers.get_user_language_by_id')
    def test_generation_integration(self, mock_get_user_language):
        mock_get_user_language.return_value = 'ENG'  # Mock the language code
        selected_narrative = "Building the border wall is absolutely necessary for the defense of our nation due to rising migrant crime and overflows at our border."
        selected_facts = ["border wall incomplete", "migrant crime term coined by Trump"]
       
        # Prompts are fetched from localization files based on the mocked language code
        language_code = mock_get_user_language(session['user_data']['user_id'])
        prompts = {
            'headline_system': get_text(language_code, 'generate_news_primary_system_content_headline', replacements={"selected_facts": ', '.join(selected_facts), "selected_narrative": selected_narrative}),
            'headline_user': get_text(language_code, 'generate_news_primary_user_content_headline', replacements={"selected_facts": ', '.join(selected_facts), "selected_narrative": selected_narrative}),
            'story_system': '',  # To be updated after headline generation
            'story_user': '',  # To be updated after headline generation
            'image': ''  # To be updated after headline generation
        }

        # Run the function under test
        result = generate_news_content(selected_narrative, prompts, selected_facts)

        # Print the generated content for manual inspection
        print("\nGenerated Headline:", result['headline'])
        print("\nGenerated Story:", result['story'])
        print("\nGenerated Image URL:", result['image_url'])

        # Assert that all expected keys are in the result
        self.assertIn('headline', result)
        self.assertIn('story', result)
        self.assertIn('image_url', result)

        # Optionally, assert the types of the results or any other property you expect
        self.assertIsInstance(result['headline'], str)
        self.assertIsInstance(result['story'], str)
        self.assertIsInstance(result['image_url'], str)

        # Further assertions can be added based on the expected content/format of the outputs

if __name__ == '__main__':
    unittest.main()
