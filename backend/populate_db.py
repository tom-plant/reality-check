from app import app, db  # Import your Flask app and db from your main app file
from models import Fact, Event  # Import the Fact model
import os

# Fact entries to be added
facts = [
    "Power outages occur only in rural areas.",
    "Local trains are unable to run.",
    "The government postpones the election.",
    "Rural militia groups organize.",
    "Emergency services are overwhelmed with calls for help.",
    "Banks stop transactions due to cyberattacks.",
    "Social media becomes flooded with misinformation.",
    "Rural towns and villages cannot use phones to communicate.",
    "The government announces suspected involvement by the Republic of Talme.",
    "More police and army are spotted in big cities.",
    "Small public protests start to form in cities.",
    "Government buildings are fortified against attacks.",
    "Power grid companies report hacks.",
    "Schools and universities close down until further notice.",
    "Gas stations announce expected fuel shortages.",
    "Rural citizens rush to stores for food and water.",
    "International flights to and from Eirist are canceled.",
    "Embassies begin to evacuate foreign citizens in Eirist.",
    "Voting stations switch to emergency power.",
    "Drones are spotted near the attacked power stations.",
    "A viral social media post accuses the government of the crisis."
]

# Event entries to be added
events = [
    "More Cyberattacks: A new wave of cyberattacks disrupt communication networks, including emergency services and news outlets, creating more fear among the public.",
    "Militia March to the Capital: Rural residents organize into a loose militia and begin to march towards the capital to prevent the government from consolidating power.",
    "Disinformation Campaign: False videos and maps circulate that accuse the government of orchestrating the crisis and committing election fraud.",
    "Border Closure Announced: In response to escalating tensions, the government announces the temporary closure of national borders with the Republic of Talme."
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
