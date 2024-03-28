from app import app, db  # Import your Flask app and db from your main app file
from models import Fact, Event  # Import the Fact model
import os

# Fact entries to be added
facts = [
    "Alarm triggered at quantum computer facility in Russia after explosion",
    "Power grids in major voting towns attacked",
    "Voting centers have switched to emergency power due to attacks",
    "Deepfake videos show current political leaders in compromised situations",
    "Public rallies between local populations break into small fights",
    "Communication blackouts disrupt emergency services",
    "Diplomats expelled from Russia over political tensions",
    "Voting systems are shut off until crisis is over",
    "Strategic reserves mobilized amidst unrest",
    "Nationwide cybersecurity alert issued",
    "Emergency curfews declared in major cities",
    "Allies withdraw aid amid diplomatic tensions",
    "Border skirmishes with Russia raise security concerns",
    "Financial markets go into a frenzy",
    "Emergency vehicles are sabotaged in key districts with cut tires",
    "Scientists debunk the possibility of quantum computer theft",
    "Public protests erupt in major cities, met with police force",
    "Air traffic control reports multiple drone sightings near airports",
    "Stock markets fluctuate wildly due to uncertainty",
    "International flights to and from the affected region suspended",

]
# Event entries to be added
events = [
    "Deepfake Campaign Exposed: A new wave of deepfake videosis detected",
    "Protest March Organized: A large-scale march to the capital city is planned, driven by grassroots movements and fueled by social media campaigns.",
    "Diplomatic Facility Siege: Protesters besiege the embassy of Russia, demanding answers and accountability for the quantum center incident.",
    "Presidential Decree Issued: The ruling party issues a controversial decree expanding executive powers, citing national security concerns.",
    "Whistleblower Assassination Attempt: An attempt on the life of the whistleblower who exposed security compromises, heightening fears of a cover-up.",
    "Border Closure Announced: In response to escalating tensions, the government announces the temporary closure of national borders.",
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
