import unittest
from flask import Flask, session
from app import db, app
from controllers import generate_secondary_narrative, generate_secondary_news_content
from config import TestingConfig
from models import User, PrimaryNarrative, FactCombination
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
app.config.from_object(TestingConfig) 

class TestGenerativeFunctionsIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()
        app.config.from_object('config.TestingConfig')  # Ensure TestingConfig is used
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI', 'your-fallback-db-uri-for-testing')

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.request_context = app.test_request_context()
        self.request_context.push()

        # Create a mock user
        self.user = User(email='test_unique@example.com', username='test_unique')
        db.session.add(self.user)
        db.session.commit()  # Commit to get the user ID

        # Create a fact combination and commit to get an ID
        self.fact_combination = FactCombination(facts=['Hamas raided Israeli village,  Israel is conducting military campaign Gaza relentlessly, Hamas is holding Israeli hostages'])
        db.session.add(self.fact_combination)
        db.session.commit()

        # Now that fact_combination has an ID, create a primary narrative
        self.primary_narrative = PrimaryNarrative(fact_combination_id=self.fact_combination.id, narrative_text='Israel is justified in its war against Gaza due to the horrific attacks on October 7 which justify immediate and swift action to eradicate the terrorists who committed this act.', user_id=self.user.id, headline="placeholder", story="placeholder", photo_url="placeholder")
        db.session.add(self.primary_narrative)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.request_context.pop()

    def test_generate_secondary_narrative_and_news_content_integration(self):
        updated_fact_combination = ['Hamas raided Israeli village, Israel is conducting military campaign Gaza relentlessly, Hamas is holding Israeli hostages, Israel reacted disproportionately, Israel targeted civilians trying to get aid']
        context = 'secondary_narrative'
        language_code = 'ENG'  # Assuming English for simplicity

        # Directly call generate_secondary_narrative
        secondary_narrative_text = generate_secondary_narrative(language_code, context, self.primary_narrative, updated_fact_combination)
        print(secondary_narrative_text)

        # Directly call generate_secondary_news_content
        news_content = generate_secondary_news_content(language_code, context, secondary_narrative_text, updated_fact_combination)
        print(news_content)

        # Assert that news content is not None and contains expected keys
        self.assertIsNotNone(news_content, "News content should not be None.")
        self.assertIn('headline', news_content, "News content should contain a headline.")
        self.assertIn('story', news_content, "News content should contain a story.")
        # Add more assertions as necessary

if __name__ == '__main__':
    unittest.main()
