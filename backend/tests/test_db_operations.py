# tests/test_db_operations.py

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from config import TestingConfig
from models import db as alchemy_db, User, Fact, Event, FactCombination, PrimaryNarrative, NarrativeEvent, SecondaryNarrative
import db_operations as db_ops


class TestCRUDOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestingConfig)  # Ensure TestingConfig has the correct settings
        alchemy_db.init_app(cls.app)

        with cls.app.app_context():  # Push an application context
            alchemy_db.create_all()  # Now you can safely access alchemy_db.engine
            cls.Session = scoped_session(sessionmaker(bind=alchemy_db.engine))

    @classmethod
    def tearDownClass(cls):
        cls.Session.remove()
        with cls.app.app_context():
            alchemy_db.drop_all()

    def setUp(self):
        self.session = self.Session()
        # Use context manager to begin a nested transaction (savepoint)
        self.trans = self.session.begin_nested()

    def tearDown(self):
        # Rollback the nested transaction
        self.session.rollback()
        self.session.close()

    # User Operations Tests
    def test_user_operations(self):
        with self.app.app_context():
            # Create
            user = db_ops.create_user('testuser', 'test@example.com', _session=self.session)
            self.session.commit()  # Ensure the user is committed
            self.assertIsNotNone(user, "Failed to create a new User.")
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'test@example.com')

            # Read by ID
            user_by_id = db_ops.get_user_by_id(user.id, _session=self.session)
            self.assertIsNotNone(user_by_id, "User creation failed or User not found.")
            self.assertEqual(user_by_id.id, user.id, "Failed to fetch User by ID.")

            # Read all users
            all_users = db_ops.get_all_users(_session=self.session)
            self.assertIn(user, all_users, "Failed to fetch all Users.")

            # Read by username
            user_by_username = db_ops.get_user_by_username('testuser', _session=self.session)
            self.assertEqual(user_by_username.username, 'testuser', "Failed to fetch User by username.")

            # Update
            db_ops.update_user(user.id, username='updateduser', email='updated@example.com', _session=self.session)
            updated_user = db_ops.get_user_by_id(user.id, _session=self.session)
            self.assertEqual(updated_user.username, 'updateduser', "Failed to update the User's username.")
            self.assertEqual(updated_user.email, 'updated@example.com', "Failed to update the User's email.")

            # Delete
            db_ops.delete_user(user.id, _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            # Clear the session to remove any cached instances
            self.session.expire_all()
            # Try to fetch the deleted user
            deleted_user = db_ops.get_user_by_id(user.id, _session=self.session)
            self.assertIsNone(deleted_user, "Failed to delete the User.")
            

    # Fact Operations Tests
    def test_fact_operations(self):
        with self.app.app_context():
            # Create
            fact = db_ops.create_fact('Fact content', 'EN', _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            self.assertIsNotNone(fact, "Failed to create a new Fact.")
            self.assertEqual(fact.text, 'Fact content')
            self.assertEqual(fact.language, 'EN')

            # Read by ID
            fact_by_id = db_ops.get_fact_by_id(fact.id, _session=self.session)
            self.assertEqual(fact_by_id.id, fact.id, "Failed to fetch Fact by ID.")

            # Read all facts
            all_facts = db_ops.get_all_facts(_session=self.session)
            self.assertIn(fact, all_facts, "Failed to fetch all Facts.")

            # Read by language
            facts_by_language = db_ops.get_facts_by_language('EN', _session=self.session)
            self.assertIn(fact, facts_by_language, "Failed to fetch Facts by language.")

            # Update
            db_ops.update_fact(fact.id, text='Updated Fact content', _session=self.session)
            updated_fact = db_ops.get_fact_by_id(fact.id, _session=self.session)
            self.assertEqual(updated_fact.text, 'Updated Fact content', "Failed to update the Fact.")

            # Delete
            db_ops.delete_fact(fact.id, _session=self.session)
            self.session.commit()  # Ensure commit here to reflect deletion
            deleted_fact = db_ops.get_fact_by_id(fact.id, _session=self.session)
            self.assertIsNone(deleted_fact, "Failed to delete the Fact.")

    # Event Operations Tests
    def test_event_operations(self):
        with self.app.app_context():
            # Create
            event = db_ops.create_event('Event Title', 'EN', _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            self.assertIsNotNone(event, "Failed to create a new Event.")
            self.assertEqual(event.text, 'Event Title')
            self.assertEqual(event.language, 'EN')

            # Read by ID
            event_by_id = db_ops.get_event_by_id(event.id, _session=self.session)
            self.assertEqual(event_by_id.id, event.id, "Failed to fetch Event by ID.")

            # Read all events
            all_events = db_ops.get_all_events(_session=self.session)
            self.assertIn(event, all_events, "Failed to fetch all Events.")

            # Read by language
            events_by_language = db_ops.get_events_by_language('EN', _session=self.session)
            self.assertIn(event, events_by_language, "Failed to fetch Events by language.")

            # Update
            db_ops.update_event(event.id, text='Updated Event Title', _session=self.session)
            updated_event = db_ops.get_event_by_id(event.id, _session=self.session)
            self.assertEqual(updated_event.text, 'Updated Event Title', "Failed to update the Event.")

            # Delete
            db_ops.delete_event(event.id, _session=self.session)
            self.session.commit()  # Ensure commit here to reflect deletion
            deleted_event = db_ops.get_event_by_id(event.id, _session=self.session)
            self.assertIsNone(deleted_event, "Failed to delete the Event.")

    # Fact Combination Operation Tests
    def test_fact_combination_operations(self):
        with self.app.app_context():
            # Create a User for testing
            user = db_ops.create_user('testuser4', 'test4@example.com', _session=self.session)
            self.session.commit()

            # Create Fact Combination
            fact_combination = db_ops.create_fact_combination('1,2,3', _session=self.session)
            self.session.commit()
            self.assertIsNotNone(fact_combination, "Failed to create a new Fact Combination.")
            self.assertEqual(fact_combination.facts, '1,2,3', "Fact Combination facts do not match.")

            # Read by ID
            fact_combination_by_id = db_ops.get_fact_combination_by_id(fact_combination.id, _session=self.session)
            self.assertEqual(fact_combination_by_id.id, fact_combination.id, "Failed to fetch Fact Combination by ID.")

            # Read all fact combinations
            all_fact_combinations = db_ops.get_all_fact_combinations(_session=self.session)
            self.assertIn(fact_combination, all_fact_combinations, "Failed to fetch all Fact Combinations.")

            # Update Fact Combination
            db_ops.update_fact_combination(fact_combination.id, '4,5,6', _session=self.session)
            updated_fact_combination = db_ops.get_fact_combination_by_id(fact_combination.id, _session=self.session)
            self.assertEqual(updated_fact_combination.facts, '4,5,6', "Failed to update the Fact Combination.")

            # Create Primary Narrative with updated Fact Combination
            narrative = db_ops.create_primary_narrative(fact_combination_id=updated_fact_combination.id, narrative_text="Sample Narrative", language="EN", user_id=user.id, headline="Sample Headline", story="Sample Story", _session=self.session)
            self.session.commit()

            # Retrieve Narratives By Fact Combination
            fact_ids = [int(fid) for fid in updated_fact_combination.facts.split(',')]  # Convert '4,5,6' to [4, 5, 6]
            narratives = db_ops.get_narratives_by_fact_combination(fact_ids, _session=self.session)
            self.assertIn(narrative, narratives, "Failed to retrieve narrative by fact combination.")

            # Delete Fact Combination
            db_ops.delete_fact_combination(fact_combination.id, _session=self.session)
            self.session.commit()
            deleted_fact_combination = db_ops.get_fact_combination_by_id(fact_combination.id, _session=self.session)
            self.assertIsNone(deleted_fact_combination, "Failed to delete the Fact Combination.")

# Primary Narrative Operation Tests
    def test_primary_narrative_operations(self):
        with self.app.app_context():
            # Assuming a user and fact_combination setup is already done
            user = db_ops.create_user('narrativeUser', 'narrative@example.com', _session=self.session)
            fact_combination = db_ops.create_fact_combination('1,2,3', _session=self.session)  # Assuming '1,2,3' represents fact IDs
            self.session.commit()  # Commit to persist data for narrative operation tests

            # Create
            primary_narrative = db_ops.create_primary_narrative(fact_combination_id=fact_combination.id, narrative_text='Sample narrative', language='EN', user_id=user.id, headline='Sample headline', story='Sample story',  photo_url='photo_url.jpg', _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            self.assertIsNotNone(primary_narrative, "Failed to create a new Primary Narrative.")
            self.assertEqual(primary_narrative.narrative_text, 'Sample narrative', "Primary Narrative text does not match.")

            # Read by ID
            primary_narrative_by_id = db_ops.get_primary_narrative_by_id(primary_narrative.id, _session=self.session)
            self.assertEqual(primary_narrative_by_id.id, primary_narrative.id, "Failed to fetch Primary Narrative by ID.")

            # Read all primary narratives
            all_primary_narratives = db_ops.get_all_primary_narratives(_session=self.session)
            self.assertIn(primary_narrative, all_primary_narratives, "Failed to fetch all Primary Narratives.")

            # Read by user
            primary_narratives_by_user = db_ops.get_primary_narratives_by_user(user.id, _session=self.session)
            self.assertIn(primary_narrative, primary_narratives_by_user, "Failed to fetch Primary Narratives by user.")

            # Update
            db_ops.update_primary_narrative(primary_narrative.id, narrative_text='Updated Narrative text', _session=self.session)
            updated_primary_narrative = db_ops.get_primary_narrative_by_id(primary_narrative.id, _session=self.session)
            self.assertEqual(updated_primary_narrative.narrative_text, 'Updated Narrative text', "Failed to update the Primary Narrative.")

            # Delete
            db_ops.delete_primary_narrative(primary_narrative.id, _session=self.session)
            self.session.commit()  # Ensure commit here to reflect deletion
            deleted_primary_narrative = db_ops.get_primary_narrative_by_id(primary_narrative.id, _session=self.session)
            self.assertIsNone(deleted_primary_narrative, "Failed to delete the Primary Narrative.")


# Narrative Event Operation Tests
    def test_narrative_event_operations(self):
        with self.app.app_context():

            # Create a user and fact_combination first
            user = db_ops.create_user('testuser2', 'test2@example.com', _session=self.session)
            self.assertIsNotNone(user, "User creation failed.")

            fact_combination = db_ops.create_fact_combination('7,8,9', _session=self.session) 
            self.assertIsNotNone(fact_combination, "FactCombination creation failed.")
            self.session.commit()  # Commit to ensure FactCombination is persisted
            self.assertIsNotNone(fact_combination.id, "FactCombination ID is None.")

            # Create a primary narrative using the `fact_combination.id` and `user.id`
            primary_narrative = db_ops.create_primary_narrative(
                fact_combination_id=fact_combination.id, 
                narrative_text='Previously generated primary narrative', 
                language='EN', user_id=user.id, headline='Sample headline', 
                story='Sample story',  
                photo_url='photo_url.jpg', 
                _session=self.session
            )
            event = db_ops.create_event('Event Title', 'EN', _session=self.session)
            self.session.commit()  # Commit to persist data for narrative event operation tests
            self.assertIsNotNone(primary_narrative, "Failed to create PrimaryNarrative.")
            self.assertIsNotNone(primary_narrative.id, "PrimaryNarrative ID is None.")

            # Create
            narrative_event = db_ops.create_narrative_event(
            primary_narrative.id, event.id, 'Headline', 'Story', 'photo_url.jpg', _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            self.assertIsNotNone(narrative_event, "Failed to create a new Narrative Event.")
            self.assertEqual(narrative_event.resulting_headline, 'Headline', "Narrative Event headline does not match.")

            # Read by ID
            narrative_event_by_id = db_ops.get_narrative_event_by_id(narrative_event.id, _session=self.session)
            self.assertEqual(narrative_event_by_id.id, narrative_event.id, "Failed to fetch Narrative Event by ID.")

            # Read all narrative events
            all_narrative_events = db_ops.get_all_narrative_events(_session=self.session)
            self.assertIn(narrative_event, all_narrative_events, "Failed to fetch all Narrative Events.")

            # Read by narrative
            narrative_events_by_narrative = db_ops.get_narrative_events_by_narrative(primary_narrative.id, _session=self.session)
            self.assertIn(narrative_event, narrative_events_by_narrative, "Failed to fetch Narrative Events by narrative.")

            # Update
            db_ops.update_narrative_event(narrative_event.id, resulting_headline='Updated Headline', _session=self.session)
            updated_narrative_event = db_ops.get_narrative_event_by_id(narrative_event.id, _session=self.session)
            self.assertEqual(updated_narrative_event.resulting_headline, 'Updated Headline', "Failed to update the Narrative Event.")

            # Delete
            db_ops.delete_narrative_event(narrative_event.id, _session=self.session)
            self.session.commit()  # Ensure commit here to reflect deletion
            deleted_narrative_event = db_ops.get_narrative_event_by_id(narrative_event.id, _session=self.session)
            self.assertIsNone(deleted_narrative_event, "Failed to delete the Narrative Event.")

# Secondary Narrative Operations
    def test_secondary_narrative_operations(self):
        with self.app.app_context():

             # Create a user and fact_combination first
            user = db_ops.create_user('testuser3', 'test3@example.com', _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            fact_combination = db_ops.create_fact_combination('10,11,12', _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            primary_narrative = db_ops.create_primary_narrative(fact_combination_id=fact_combination.id, 
                narrative_text='Previously generated primary narrative', 
                language='EN', 
                user_id=user.id, 
                headline='Sample headline', 
                story='Sample story', 
                photo_url='photo_url.jpg', 
                _session=self.session
            )
            self.session.commit()  # Commit to persist data for secondary narrative operation tests

            # Create
            secondary_narrative = db_ops.create_secondary_narrative(
                primary_narrative.id, 'Updated Fact Combination', 'Secondary Narrative text',
                'Secondary Headline', 'Secondary Story', 'secondary_photo_url.jpg', _session=self.session)
            self.session.commit()  # Commit to persist data for read operation tests
            self.assertIsNotNone(secondary_narrative, "Failed to create a new Secondary Narrative.")
            self.assertEqual(secondary_narrative.narrative_text, 'Secondary Narrative text', "Secondary Narrative text does not match.")

            # Read by ID
            secondary_narrative_by_id = db_ops.get_secondary_narrative_by_id(secondary_narrative.id, _session=self.session)
            self.assertEqual(secondary_narrative_by_id.id, secondary_narrative.id, "Failed to fetch Secondary Narrative by ID.")

            # Read all secondary narratives
            all_secondary_narratives = db_ops.get_all_secondary_narratives(_session=self.session)
            self.assertIn(secondary_narrative, all_secondary_narratives, "Failed to fetch all Secondary Narratives.")

            # Read by original narrative
            secondary_narratives_by_original = db_ops.get_secondary_narratives_by_original_narrative(
                primary_narrative.id, _session=self.session)
            self.assertIn(secondary_narrative, secondary_narratives_by_original, "Failed to fetch Secondary Narratives by original narrative.")

            # Update
            db_ops.update_secondary_narrative(secondary_narrative.id, narrative_text='Updated Secondary Narrative text', _session=self.session)
            updated_secondary_narrative = db_ops.get_secondary_narrative_by_id(secondary_narrative.id, _session=self.session)
            self.assertEqual(updated_secondary_narrative.narrative_text, 'Updated Secondary Narrative text', "Failed to update the Secondary Narrative.")

            # Delete
            db_ops.delete_secondary_narrative(secondary_narrative.id, _session=self.session)
            self.session.commit()  # Ensure commit here to reflect deletion
            deleted_secondary_narrative = db_ops.get_secondary_narrative_by_id(secondary_narrative.id, _session=self.session)
            self.assertIsNone(deleted_secondary_narrative, "Failed to delete the Secondary Narrative.")

            
if __name__ == '__main__':
    unittest.main()
