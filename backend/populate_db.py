from app import app, db  # Import your Flask app and db from your main app file
from models import Fact, Event  # Import the Fact model
import os

# Fact entries to be added
facts = [
    "Quantum computing center alarm activated in China.",
    "A domestic terrorist group claims responsibility online.",
    "Power grids targeted, causing widespread blackouts.",
    "Political rallies canceled amid security concerns.",
    "Government invokes emergency powers, citing national security.",
    "Emergency services overwhelmed by simultaneous incidents.",
    "National ID database compromised, personal data leaked.",
    "Critical infrastructure control systems report malfunctions.",
    "Unusual troop movements observed near key facilities.",
    "Scientists debunk the possibility of quantum computer theft.",
    "Border security intensifies, with increased checks and patrols.",
    "Government tightens control over media and internet access.",
    "Key public figures receive anonymous threats.",
    "Public protests erupt in major cities, met with police force.",
    "Foreign diplomats express concern, offer vague support.",
    "Air traffic control reports multiple drone sightings near airports.",
    "Infrastructure sabotage reported in strategic locations.",
    "Citizens report mysterious drone sightings over key facilities.",
    "Stock markets fluctuate wildly due to uncertainty.",
    "International flights to and from the affected region suspended.",
    "Cryptocurrency transactions spike amid bank network failures.",
    "Emergency broadcast systems activated, issuing vague warnings.",
    "Increased military presence noted in urban areas.",
    "Hospitals report a surge in patients with stress-related conditions.",
    "School closures announced nationwide due to security concerns."
]
# Event entries to be added
events = [
    "The President invokes an 'imperial presidency' to unify power amidst national security concerns.",
    "A high-profile whistleblower from within the government leaks documents suggesting the quantum breach was known and contained.",
    "Terrorist group leaks set of photos shows the alleged top secret chinese quantum computing center",
]


if os.getenv('FLASK_ENV') == 'development':
    with app.app_context():  # Use the app's context
        # Iterate over the facts list and add each to the database
        for fact_text in facts:
            new_fact = Fact(text=fact_text, language='ENG')  # Assuming all facts are in English
            db.session.add(new_fact)
        for event_text in events:
            new_event = Event(text=event_text, language='ENG')  # Assuming all facts are in English
            db.session.add(new_event)
        # Commit the session to save these objects to the database
        db.session.commit()

print("Database populated with facts and events.")
