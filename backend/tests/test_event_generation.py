import unittest
from flask import Flask, session
from app import db  # Ensure this import matches your project structure
from controllers import generate_event_news_content, generate_news_content  # Update with the correct import path
from config import TestingConfig
from unittest.mock import patch


app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

# Define the mock class here, at the top level
class MockNarrativeEvent:
    def __init__(self, id=None, narrative_id=None, event_id=None):
        self.id = id
        self.narrative_id = narrative_id
        self.event_id = event_id
        self.resulting_headline = None
        self.resulting_story = None
        self.resulting_photo_url = None

class TestGenerateAndStoreNewsContentRealAPI(unittest.TestCase):

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
    def test_generate_event_news_content_real_api(self, mock_get_user_language):
        mock_get_user_language.return_value = 'ENG'  # Mock the language code
        
        selected_narrative = "Russia is fighting in Ukraine to take back the land that it once owned and liberate the Russian people there from the oppressive and corrupt leadership in Ukraine."
        selected_facts = ["During combat, a stray missile lands in Poland"]
        context = "events_narrative"  # Context for the narrative

        # Create a dummy narrative_event for the purpose of this test
        narrative_event = MockNarrativeEvent()

        print("Language Code:", 'ENG')
        print("Context:", context)
        print("Selected Narrative:", selected_narrative)
        print("Selected Facts:", selected_facts)
        print("Narrative Event:", narrative_event)

        # Run the function under test with the selected narrative, context, and facts
        result = generate_event_news_content(selected_narrative, context, 'ENG', selected_facts, narrative_event)

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
        # Assert the image URL format or content if there's a predictable pattern
        self.assertTrue(result['image_url'].startswith('http'))

        # Further assertions can be based on the expected content/format of the outputs

        print("Result:", result)
        if result is not None:
            print("Generated Headline:", result.get('headline'))
            print("Generated Story:", result.get('story'))
            print("Generated Image URL:", result.get('image_url'))
        else:
            print("Result is None")


if __name__ == '__main__':
    unittest.main()
