#app.py 

from flask import Flask, session, jsonify, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session 
from models import db  # Import the db instance from models.py
import uuid #for unique user id
from config import Config, FLASK_KEY, SQL_KEY
from controllers import * 

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        # Delegate to the controller function
        return register_user(username, email)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        # Delegate to the controller function
        return login_user(username_or_email)
    return render_template('login.html')

@app.route('/logout')
def logout():
    return logout_user()


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
    print("Route /game/introduce_event is being called")  # This should print if the route is hit
    # Call the introduce_event_controller function to handle the logic
    response_data, status_code = introduce_event_controller()
    
    # Return response to frontend with the appropriate status code
    return jsonify(response_data), status_code

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

