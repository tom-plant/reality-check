# tests/test_db_operations.py

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from config import TestingConfig
from models import db as alchemy_db, User, PrimaryNarrative, SecondaryNarrative, Fact, Event, NarrativeFactAssociation
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


    def test_primary_narrative_operations(self):
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            self.session.add(user)
            self.session.commit()

            # Create
            db_ops.create_primary_narrative('Narrative', 'Headline', 'Story', 'Photo', user.id, _session=self.session)
            narrative = self.session.query(PrimaryNarrative).first()
            self.assertIsNotNone(narrative)

            # Read
            retrieved_narrative = db_ops.get_primary_narrative_by_id(narrative.id, _session=self.session)
            self.assertEqual(retrieved_narrative.id, narrative.id)

            # Update
            db_ops.update_primary_narrative(narrative.id, 'Updated Narrative', 'Updated Headline', 'Updated Story', 'Updated Photo', _session=self.session)
            updated_narrative = self.session.get(PrimaryNarrative, narrative.id)  
            self.assertEqual(updated_narrative.narrative, 'Updated Narrative')

            # Delete
            db_ops.delete_primary_narrative(narrative.id, _session=self.session)
            deleted_narrative = self.session.get(PrimaryNarrative, narrative.id)
            self.assertIsNone(deleted_narrative)

    def test_secondary_narrative_operations(self):
        with self.app.app_context():
            user = User(username='testuser2', email='test2@example.com')
            self.session.add(user)
            self.session.commit()

            primary_narrative = PrimaryNarrative(narrative='Primary', headline='Primary Headline', news_story='Primary Story', photo='Primary Photo', user_id=user.id)
            self.session.add(primary_narrative)
            self.session.commit()

            event = Event(event='Event', language='EN')
            self.session.add(event)
            self.session.commit()

            # Create
            db_ops.create_secondary_narrative(primary_narrative.id, event.id, 'Secondary Narrative', 'Outcome', _session=self.session)
            secondary_narrative = self.session.query(SecondaryNarrative).first()
            self.assertIsNotNone(secondary_narrative)

            # Read
            retrieved_secondary_narrative = db_ops.get_secondary_narrative_by_id(secondary_narrative.id, _session=self.session)
            self.assertEqual(retrieved_secondary_narrative.id, secondary_narrative.id)

            # Update
            db_ops.update_secondary_narrative(secondary_narrative.id, primary_narrative.id, event.id, 'Updated Secondary Narrative', 'Updated Outcome', _session=self.session)
            updated_secondary_narrative = self.session.get(SecondaryNarrative, secondary_narrative.id)
            self.assertEqual(updated_secondary_narrative.narrative, 'Updated Secondary Narrative')

            # Delete
            db_ops.delete_secondary_narrative(secondary_narrative.id, _session=self.session)
            deleted_secondary_narrative = self.session.get(SecondaryNarrative, secondary_narrative.id)
            self.assertIsNone(deleted_secondary_narrative)

    def test_fact_operations(self):
        with self.app.app_context():
            # Create Fact
            fact = Fact(fact='Fact content', language='EN', is_key_fact=True)
            self.session.add(fact)
            self.session.commit()

            # Read Fact by Language
            facts = db_ops.get_facts_by_language('EN', _session=self.session)
            self.assertEqual(len(facts), 1)
            self.assertEqual(facts[0].fact, 'Fact content')

    def test_event_operations(self):
        with self.app.app_context():
            # Create Event
            event = Event(event='Event content', language='EN')
            self.session.add(event)
            self.session.commit()

            # Read Event by Language
            events = db_ops.get_events_by_language('EN', _session=self.session)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].event, 'Event content')

    def test_get_narratives_by_unassociated_facts(self):
        with self.app.app_context():
            # Setup - create user, facts, and a narrative without associations
            user = User(username='testuser3', email='test3@example.com')
            fact1 = Fact(fact='Fact 1', language='EN', is_key_fact=True)
            fact2 = Fact(fact='Fact 2', language='EN', is_key_fact=False)
            narrative = PrimaryNarrative(narrative='Unassociated Narrative', headline='Headline', news_story='Story', photo='Photo', user_id=user.id)
            self.session.add_all([user, fact1, fact2, narrative])
            self.session.commit()

            # Call the function with the ids of the unassociated facts
            unassociated_facts_ids = [fact1.id, fact2.id]
            narratives = db_ops.get_narratives_by_facts(unassociated_facts_ids, _session=self.session)

            # Assert that the result is an empty list, as there are no narratives associated with these facts
            self.assertEqual(len(narratives), 0, "Expected to find no narratives associated with the given fact IDs")

    def test_narrative_fact_association_operations(self):
        with self.app.app_context():
            # Setup for association test
            user = User(username='assocUser', email='assocUser@example.com')
            primary_narrative = PrimaryNarrative(narrative='Assoc Narrative', headline='Assoc Headline', news_story='Assoc Story', photo='Assoc Photo', user_id=user.id)
            fact1 = Fact(fact='Assoc Fact 1', language='EN', is_key_fact=True)
            fact2 = Fact(fact='Assoc Fact 2', language='EN', is_key_fact=False)
            self.session.add_all([user, primary_narrative, fact1, fact2])
            self.session.commit()

            # Update Narrative-Fact Association
            db_ops.update_narrative_association(primary_narrative.id, [fact1.id, fact2.id], _session=self.session)

            # Verify associations have been created
            associations = self.session.query(NarrativeFactAssociation).filter_by(narrative_id=primary_narrative.id).all()
            # print(f"Associations for narrative {primary_narrative.id}:")
            # for assoc in associations:
            #     print(f"- Fact ID: {assoc.fact_id}")

            self.assertTrue(fact1.id in [assoc.fact_id for assoc in associations])
            self.assertTrue(fact2.id in [assoc.fact_id for assoc in associations])

            # Print existing associations for debugging
            # associations = self.session.query(NarrativeFactAssociation).filter_by(narrative_id=primary_narrative.id).all()
            # print("Existing associations after update:", len(associations))
            # for assoc in associations:
                # print(f"Narrative ID: {assoc.narrative_id}, Fact ID: {assoc.fact_id}")
            
            # Directly query NarrativeFactAssociation table to ensure associations exist
            # associations = self.session.query(NarrativeFactAssociation).filter(NarrativeFactAssociation.narrative_id == primary_narrative.id).all()
            # print("Direct query associations count:", len(associations))
            # for assoc in associations:
                # print(f"Direct query - Narrative ID: {assoc.narrative_id}, Fact ID: {assoc.fact_id}")

            # Read Narratives by Facts
            narratives = db_ops.get_narratives_by_facts([fact1.id, fact2.id], _session=self.session)
            self.assertEqual(len(narratives), 1)
            self.assertEqual(narratives[0].id, primary_narrative.id)
            
if __name__ == '__main__':
    unittest.main()
