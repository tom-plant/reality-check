import unittest
from flask import Flask, session
from app import db
from controllers import generate_news_content, generate_and_store_news_content
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
            'language': 'EST',  
            'fact_combination_id': 'some_fact_combination_id'  
            'primary_narrative_id': '1'  
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if self.request_context:
            self.request_context.pop()
        self.app_context.pop()


    def test_generate_and_store_news_content_with_api(self):
        # Setup test data
        narrative_event = "Dummy Event and News Stored in Dataset"  # Placeholder for the narrative event object
        selected_narrative = "Building the border wall is absolutely necessary for the defense of our nation due to rising migrant crime and overflows at our border."
        event = "Oil tanker leaks in the Gulf of Mexico, washing oil on both sides of the US-Mexico border"
        selected_facts = ["border wall incomplete", "migrant crime term coined by Trump"]
        language_code = session['user_data']['language_code']

        # Prepare prompts for content generation, assuming these are needed for the API call
        prompts = {
            "headline_system": get_text(language_code, 'generate_news_events_system_content_headline', replacements={"selected_narrative": selected_narrative, "event": event}),
            "headline_user": get_text(language_code, 'generate_news_events_user_content_headline', replacements={"selected_narrative": selected_narrative, "event": event}),
        }

        # Execute the function under test
        result = generate_and_store_news_content(narrative_event, selected_narrative, event, language_code, selected_facts)

        # Assert the structure and content of the result
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('headline', result)
        self.assertIn('story', result)
        self.assertTrue(result['headline'])  # Ensure the headline is not empty
        self.assertTrue(result['story'])  # Ensure the story is not empty

        # If the function is expected to return a photo URL, assert it
        if 'photo_url' in result:
            self.assertTrue(result['photo_url'].startswith('http'))

if __name__ == '__main__':
    unittest.main()