from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config, FLASK_KEY, SQL_KEY
import uuid #for unique user id
from flask_migrate import Migrate
from models import db  # Import the db instance from models.py
from flask_session import Session 

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://reality_check_user:Eesti_$imulat10n@localhost/reality_check' ##Switch this eventually
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy instance
db.init_app(app)

# Initialize Flask-Migrate associated with app and SQLAlchemy instance
migrate = Migrate(app, db)

#Initialize session management tools
app.secret_key = FLASK_KEY
def generate_session_id():
    return str(uuid.uuid4())

from flask import request, jsonify

@app.route('/')
def index():
    # Generate session ID for the user
    session_id = generate_session_id()

    # Store session ID in session
    session['session_id'] = session_id

    return f'Session ID generated: {session_id}'

# Initial Fact Selection & Narrative Generation
@app.route('/game/select_facts', methods=['POST'])
def select_facts():
    # Receive selected facts from the frontend
    selected_facts = request.json.get('selected_facts')
    
    # Call controller function to handle logic
    response_data = select_facts_controller(selected_facts)
    
    # Return response to frontend
    return jsonify(response_data)

# Selecting Narratives
@app.route('/game/select_narrative', methods=['POST'])
def select_narrative():
    # Receive selected narrative and facts combination from the frontend
    selected_narrative = request.json.get('selected_narrative')
    selected_facts = request.json.get('selected_facts')
    
    # Call controller function to handle logic
    response_data = select_narrative_controller(selected_narrative, selected_facts)
    
    # Return response to frontend
    return jsonify(response_data)

# Introducing Follow-up Events
@app.route('/game/introduce_event', methods=['GET'])
def introduce_event():
    # Call controller function to handle logic
    # Placeholder for controller function
    response_data = introduce_event_controller()
    
    # Return response to frontend
    return jsonify(response_data)

# Identifying Weaknesses in Narratives
@app.route('/game/identify_weaknesses', methods=['POST'])
def identify_weaknesses():
    # Receive new combination of facts and narrative from the frontend
    new_facts = request.json.get('new_facts')
    narrative = request.json.get('narrative')
    
    # Call controller function to handle logic
    # Placeholder for controller function
    response_data = identify_weaknesses_controller(new_facts, narrative)
    
    # Return response to frontend
    return jsonify(response_data)

# Saving User Progress
@app.route('/game/save_progress', methods=['POST'])
def save_progress():
    # Receive user progress data from the frontend
    user_progress = request.json.get('user_progress')
    
    # Call controller function to handle logic
    # Placeholder for controller function
    response_data = save_progress_controller(user_progress)
    
    # Return response to frontend
    return jsonify(response_data)
    
# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)

