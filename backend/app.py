from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import API_KEY, FLASK_KEY, SQL_KEY
import uuid #for unique user id

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://reality_check_user:Eesti_$imulat10n@localhost/reality_check' ##Switch this eventually
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy instance
db = SQLAlchemy(app)

#Initialize session management tools
app.secret_key = FLASK_KEY
def generate_session_id():
    return str(uuid.uuid4())



@app.route('/')
def index():
    # Generate session ID for the user
    session_id = generate_session_id()

    # Store session ID in session
    session['session_id'] = session_id

    # return f'Session ID generated: {session_id}'

@app.route('/game/select_facts', methods=['POST'])
def select_facts():
    # Handle logic for selecting important information
    return "Selected facts received and processed"

@app.route('/game/select_narrative', methods=['POST'])
def select_narrative():
    # Handle logic for selecting narratives
    return "Selected narrative received and stored"

@app.route('/game/introduce_event')
def introduce_event():
    # Handle logic for introducing follow-up events
    return "Follow-up event introduced"

@app.route('/game/identify_weaknesses', methods=['POST'])
def identify_weaknesses():
    # Handle logic for identifying weaknesses in narratives
    return "Identified weaknesses in narrative"

@app.route('/game/save_progress', methods=['POST'])
def save_progress():
    # Handle logic for saving user progress
    return "User progress saved"
    
# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)

