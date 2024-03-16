#app.py 

from flask import Flask, session, jsonify, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session 
from models import db  
from flask_cors import CORS
import uuid #for unique user id
from config import Config, DevelopmentConfig, TestingConfig, SECRET_KEY, SQL_KEY
from controllers import * 
from dotenv import load_dotenv
import os


load_dotenv()  # This loads the variables from .env into the environment

app = Flask(__name__)
if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(Config)  # Default to Config if not specified
CORS(app, resources={r"/*": {"origins": os.environ.get('ALLOWED_ORIGINS')}})
Session(app)

# Initialize SQLAlchemy instance
db.init_app(app)

# Initialize Flask-Migrate associated with app and SQLAlchemy instance
migrate = Migrate(app, db)

#Initialize session management tools
app.secret_key = SECRET_KEY
def generate_session_id():
    return str(uuid.uuid4())

@app.route('/')
def hello():
    return "Hello, Dockerized Flask!"

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    # Delegate to the controller function
    response, status = register_user(username, email)  
    return jsonify(response), status

@app.route('/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # Your login logic here: validate the user and create a token or session
    token = login_user_controller(username, password)  # Ensure this controller exists and handles authentication
    if token:
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()  # This clears all items in the session
    return jsonify({"message": "User logged out successfully"}), 200

    
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
@app.route('/game/introduce_event', methods=['POST'])
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
    response_data = identify_weaknesses_controller(updated_fact_combination)
    
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

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error="Bad Request"), 400

@app.errorhandler(500)
def server_error(e):
    return jsonify(error="Internal Server Error"), 500
    
# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
