import unittest
from unittest.mock import patch
from flask import Flask, session
from app import db
from controllers import select_narrative_controller  # Ensure this is the correct import
from config import TestingConfig, FLASK_KEY

app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

class TestSelectNarrativeController(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.secret_key = FLASK_KEY
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_user_not_logged_in(self):
        with app.test_request_context():
            response = select_narrative_controller('selected_narrative', ['fact1', 'fact2'])
            self.assertEqual(response, ({"error": "User not logged in"}, 401))

    def test_narrative_and_facts_stored_successfully(self):
        with app.test_request_context():
            # Directly setting the user_id in session for this test
            session['user_id'] = 'user_id'
            response = select_narrative_controller('selected_narrative', ['fact1', 'fact2'])
            self.assertEqual(response, {"message": "Narrative and facts selection processed successfully"})
            self.assertEqual(session['selected_narrative'], 'selected_narrative')
            self.assertEqual(session['selected_facts'], ['fact1', 'fact2'])

if __name__ == '__main__':
    unittest.main()
