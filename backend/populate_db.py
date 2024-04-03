from app import app, db  # Import your Flask app and db from your main app file
from models import Fact, Event  # Import the Fact model
import os

# Fact entries to be added
facts = [
    "Alarm triggered at quantum computer facility in the Republic of Talme.",
    "Massive power outages plunges the rural areas across Eirist into total darkness.",
    "Voting centers switch to emergency power due to attacks.",
    "Some members of the government are calling to cancel the election.",
    "Deepfake videos show current political leaders in compromised situations.",
    "Local populations break into small fights, blaming each other for the power outages.",
    "Communication blackouts disrupt emergency services.",
    "Eirist diplomats are called back from the Republic of Talme.",
    "Third-party fact checkers reveal various parts of the crisis to be AI-generated.",
    "Voting systems are shut off until crisis is over.",
    "The government postpones elections for a week.",
    "The Eirist military is mobilized amidst unrest.",
    "Nationwide cybersecurity alert issued.",
    "Emergency curfews declared in major cities.",
    "Allies withdraw aid amid diplomatic tensions.",
    "Border skirmishes with The Republic of Talme raise security concerns.",
    "Financial markets go into a frenzy.",
    "The power stations were attacked with small, hand-made explosives, not cyber weapons.",
    "Emergency vehicles are sabotaged in key districts with cut tires.",
    "Data leaks expose emails of rural Eirist citizens.",
    "Drones are spotted near the attacked power stations.",
    "Emergency alerts sent to leaked emails about an attack by the Republic of Talme.",
    "The data leaks contain already publicly-available data.",
    "Suspicious packages are found near critical infrastructure sites.",
    "Journalists from the Republic of Talme are expelled from Eirist under suspicion of espionage.",
    "Roadblocks and obstacles appear in cities, blocking streets.",
    "Public transportation systems experience widespread disruptions.",
    "Scattered reports emerge of individuals claiming responsibility for the attacks.",
    "Emergency services receive reports of imminent attacks on Eirist.",
    "A viral social media post says the Eirist government orchestrated the crisis to stay in power"
    ]

# Event entries to be added
events = [
    "Deepfake Campaign Exposed: A new wave of deepfake videos is unveiled, throwing everything in the media into uncertainty",
    "Extremist Group Takes Credit: A viral video depicts an Eirist militia group taking credit for the attacks",
    "Protest March Organized: A large-scale march from the rural areas impacted by the blackout to the capital of Eirist is planned.",
    "Diplomatic Facility Siege: Protesters besiege the Embassy of the Republic of Talme, demanding answers and accountability for the quantum center incident.",
    "Presidential Decree Issued: The Eirist Government issues a controversial decree expanding executive powers, citing national security concerns.",
    "Assassination Attempt: An attempt on the life of a high-ranking official occurs.",
    "Border Closure Announced: In response to escalating tensions, the government announces the temporary closure of national borders with the Republic of Talme.",
]


if os.getenv('FLASK_ENV') == 'production':
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
