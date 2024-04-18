from app import app, db  # Import your Flask app and db from your main app file
from models import Fact, Event, Actor, Strat, CounterStrat, StrategyEffectiveness # Import the Fact model
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

actors = [
    "Eirist Government: The ruling body of Eirist up for re-election.",
    "Rural Militias: Loosely organized groups formed in rural areas, consisting of conservative voters and immigrant populations.",
    "Republic of Talme: Foreign nation with a poor relationship to Eirist.",
    "Eirist Opposition Parties: Political parties opposing the current Eirist government, seeking to gain power in the upcoming elections.",
    "International Community: Global entities and foreign nations observing and potentially intervening in Eirist's crisis.",
]

strats = [
    "Showing the Cause-and-Effect: Saying one event caused another without sufficient detail to connect the two events.",
    "Instructing What to Believe: Directly telling the reader what is correct and incorrect.",
    "Highlighting Danger: Focusing on risks to guide readers to a belief based on emotions, like fear. ",
    "Appealing to Personal Beliefs: Connecting the reader’s existing beliefs to a particular understanding of an event.",
]

counterstrats = [
    "Offering an Alternative Explanation: Presenting an alternative explanation to the inaccurate one without explicitly correcting it.",
    "Debunking the False Claim: Providing thorough reasoning to disprove misleading information.",
    "Recalibrating Emotions and Framing: Using a correction to validate the reader's existing beliefs and reassure their interests.",
    "Corrective Data Aligned with Personal Values: Offering data and evidence from trusted sources to back up true claims.",
]

effectiveness_mappings = [
    ('strong', 'medium', 'weak', 'medium'),  # For Showing the Cause-and-Effect
    ('weak', 'strong', 'medium', 'medium'),  # For Instructing What to Believe
    ('medium', 'medium', 'strong', 'weak'),  # For Highlighting Danger
    ('medium', 'weak', 'medium', 'strong')   # For Appealing to Personal Beliefs
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
        for actor_text in actors:
            new_actor = Actor(text=actor_text, language='ENG')  # Assuming all facts are in English
            db.session.add(new_actor)
        for strat_text in strats:
            new_strat = Strat(text=strat_text, language='ENG')  # Assuming all facts are in English
            db.session.add(new_strat)
        for counterstrat_text in counterstrats:
            new_counterstrat = CounterStrat(text=counterstrat_text, language='ENG')  # Assuming all facts are in English
            db.session.add(new_counterstrat)
        # Commit the session to save these objects to the database
        db.session.commit()

        # Retrieve all strategies and counterstrategies
        strats_db = {strat.text: strat.id for strat in Strat.query.all()}
        counterstrats_db = {cstrat.text: cstrat.id for cstrat in CounterStrat.query.all()}

        # Prepare StrategyEffectiveness entries
        effectiveness_entries = []
        for idx, (strat, effects) in enumerate(zip(strats, effectiveness_mappings)):
            for jdx, eff in enumerate(effects):
                effectiveness_entries.append({
                    'strategy_id': strats_db[strat],
                    'counter_strategy_id': counterstrats_db[counterstrats[jdx]],
                    'effectiveness': eff
                })

        # Bulk insert StrategyEffectiveness entries
        db.session.bulk_insert_mappings(StrategyEffectiveness, effectiveness_entries)
        db.session.commit()

print("Database populated with facts and events.")
