#app.py 

from flask import Flask, session, jsonify, redirect, url_for, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session 
from models import db  
from db_operations import *
from flask_cors import CORS
import uuid #for unique user id
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig, SECRET_KEY, SQL_KEY
from controllers import initialize_data_controller, register_user_controller, get_all_facts_controller, get_all_events_controller, select_facts_controller, select_narrative_controller, introduce_event_controller, identify_weaknesses_controller
from dotenv import load_dotenv
import os
import sys
from sqlalchemy.exc import SQLAlchemyError
import logging


# Determine which environment to load
load_dotenv()

print('Database URI:', os.getenv('SQLALCHEMY_DATABASE_URI'))

app = Flask(__name__, static_folder='build/static')

if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestingConfig)
elif os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(Config)  # Default to Config if not specified

print('Configured Database URI:', app.config['SQLALCHEMY_DATABASE_URI'])

CORS(app, supports_credentials=True, resources={r"/*": {"origins": os.environ.get('ALLOWED_ORIGINS')}})
Session(app)

# Initialize Flask-Migrate associated with app and SQLAlchemy instance
migrate = Migrate(app, db)
db.init_app(app)

# Make sure we can read print statements for debugging
app.debug = True
app.logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG


#Initialize session management tools
app.secret_key = SECRET_KEY
def generate_session_id():
    return str(uuid.uuid4())
        
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory('build', 'index.html')

@app.route('/')
def hello():
    return "Hello, Dockerized Flask!"

@app.route('/debug/session')
def debug_session():
    return jsonify(dict(session))

@app.route('/auth', methods=['POST'])
def auth():
    username = request.json.get('username')
    email = request.json.get('email')

    # Check if the user exists by email
    existing_user = get_user_by_email(email)

    if existing_user:
        # If the user exists, check if the username matches
        if existing_user.username == username:
            # Proceed with login
            initialize_data_controller(existing_user.id)
            session['user_id'] = existing_user.id
            return jsonify({"message": "User logged in successfully", "user_id": existing_user.id})
        else:
            # Username does not match the existing record
            return jsonify({"error": "Username and email do not match."})
    else:
        # Proceed with registration if the user does not exist
        try:
            response = register_user_controller(username, email)
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": "User registration failed", "details": str(e)})


@app.route('/game/get_facts', methods=['GET'])
def get_facts():
    response_data = get_all_facts_controller()
    return jsonify(response_data)

@app.route('/game/get_events', methods=['GET'])
def get_events():
    response_data = get_all_events_controller()
    return jsonify(response_data)

    
# Initial Fact Selection & Narrative Generation
@app.route('/game/select_facts', methods=['POST'])
def select_facts():
    try: 
        # Receive selected facts from the frontend
        selected_facts = request.json.get('selected_facts')
        # Call controller function to handle logic
        response_data = select_facts_controller(selected_facts)
        # Return response to frontend
        return jsonify(response_data)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database operation failed"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# Selecting Narratives
@app.route('/game/select_narrative', methods=['POST'])
def select_narrative():
    # Receive selected narrative from the frontend
    selected_narrative = request.json.get('selected_narrative')
    
    # Call controller function to handle logic
    response_data = select_narrative_controller(selected_narrative)
    
    # Return response to frontend
    return jsonify(response_data)

# Introducing Follow-up Events
@app.route('/game/introduce_event', methods=['POST'])
def introduce_event():
    # Receive event from the frontend
    Event = request.json.get('Event')
    
    # Call the introduce_event_controller function to handle the logic
    response_data = introduce_event_controller(Event)
    
    # Return response to frontend with the appropriate status code
    return jsonify(response_data)

# Identifying Weaknesses in Narratives
@app.route('/game/identify_weaknesses', methods=['POST'])
def identify_weaknesses():
    # Receive new combination of facts from the frontend
    updated_fact_combination = request.json.get('updated_fact_combination')
    
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
