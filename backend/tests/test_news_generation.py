import unittest
from flask import Flask, session
from app import db
from controllers import generate_news_content  
from localization import get_text
from config import TestingConfig

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
        session['user_data'] = {
            'user_id': '1',
            'language': 'EST',  # Assuming default language is English
            'fact_combination_id': 'some_fact_combination_id'  # Assuming this is required and has a default or test value
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if self.request_context:
            self.request_context.pop()
        self.app_context.pop()

    def test_generation_integration(self):
        # Assuming 'selected_narrative' and 'selected_facts' are required for the function
        selected_narrative = "Building the border wall is absolutely necessary for the defense of our nation due to rising migrant crime and overflows at our border."
        selected_facts = ["border wall incomplete", "migrant crime term coined by Trump"]

        # Assuming prompts are fetched from localization files based on session language and other parameters
        prompts = {
            'headline_system': get_text(session['user_data']['language'], 'generate_news_headline_system', {}),
            'headline_user': get_text(session['user_data']['language'], 'generate_news_headline_user', {}),
            'story_system': get_text(session['user_data']['language'], 'generate_news_story_system', {'selected_narrative': selected_narrative, 'selected_facts': ', '.join(selected_facts)}),
            'story_user': get_text(session['user_data']['language'], 'generate_news_story_user', {'selected_narrative': selected_narrative, 'selected_facts': ', '.join(selected_facts)}),
            'image': ''  # The 'image' prompt will be updated within the function based on the generated headline
        }

        # Run the function under test
        print("selected_facts in test:", selected_facts, type(selected_facts))
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
