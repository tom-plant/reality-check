#app.py 

from flask import Flask, session, jsonify, redirect, url_for, render_template, request, send_from_directory
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig, SECRET_KEY, SQL_KEY
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session 
from flask_cors import CORS
import uuid #for unique user id
from dotenv import load_dotenv
import os
import sys
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
import logging


# Initialize Flask app
app = Flask(__name__, static_folder='build/static')

# Determine which environment to load and apply configurations
load_dotenv()
if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestingConfig)
elif os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(Config)  # Default to Config if not specified

print('Configured Database URI:', app.config['SQLALCHEMY_DATABASE_URI'])

# Initialize SQLAlchemy with app
db = SQLAlchemy(app)

# Initialize Flask-Migrate with app and db
migrate = Migrate(app, db)

# Enable CORS and Session
CORS(app, supports_credentials=True, resources={r"/*": {"origins": os.environ.get('ALLOWED_ORIGINS')}})
Session(app)

# Make sure we can read print statements for debugging
app.debug = True
app.logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

from models import * 
from controllers import initialize_data_controller, register_user_controller, get_all_facts_controller, get_all_events_controller, get_all_actors_controller, get_all_strats_controller, get_all_counterstrats_controller, select_facts_controller, build_narrative_controller, select_narrative_controller, introduce_event_controller, identify_weaknesses_controller, conclusion_controller
from db_operations import *  

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

@app.route('/game/get_actors', methods=['GET'])
def get_actors():
    response_data = get_all_actors_controller()
    return jsonify(response_data)

@app.route('/game/get_strats', methods=['GET'])
def get_strats():
    response_data = get_all_strats_controller()
    return jsonify(response_data)

@app.route('/game/get_counterstrats', methods=['GET'])
def get_counterstrats():
    response_data = get_all_counterstrats_controller()
    return jsonify(response_data)

# Initial Fact Selection & Narrative Generation
@app.route('/game/select_facts', methods=['POST'])
def select_facts():
    try: 
        # Retrieve selected facts from the frontend
        selected_facts = request.json.get('selected_facts')
        # Call controller function to handle logic
        select_facts_controller(selected_facts)
        # No response data needed for GET method
        return '', 200
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database operation failed"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# Building Narrative
@app.route('/game/build_narrative', methods=['POST'])
def build_narrative():
    # Receive selected actor and strategies from the frontend
    selected_actor = request.json.get('selected_actor')
    selected_strategies = request.json.get('selected_strategies')
    
    # Call the build_narrative_controller function to handle the logic
    response_data = build_narrative_controller(selected_actor, selected_strategies)
    
    # Return response to frontend
    return jsonify(response_data)

# Selecting Narratives
@app.route('/game/select_narrative', methods=['POST'])
def select_narrative():
    # Receive selected narrative and strategy from the frontend
    data = request.get_json()
    narrative = data['narrative']
    strategy = data['strategy']
    
    # Call controller function to handle logic
    response_data = select_narrative_controller(narrative, strategy)
    return jsonify(response_data)

# Introducing Follow-up Events
@app.route('/game/introduce_event', methods=['POST'])
def introduce_event():
    # Receive event from the frontend
    event_details = request.json.get('event_details')
    
    # Call the introduce_event_controller function to handle the logic
    response_data = introduce_event_controller(event_details)
    
    # Return response to frontend with the appropriate status code
    return jsonify(response_data)


# Identifying Weaknesses in Narratives
@app.route('/game/identify_weaknesses', methods=['POST'])
def identify_weaknesses():
    # Receive updated fact combination and selected strategies from the frontend
    updated_fact_combination = request.json.get('updated_fact_combination')
    selected_strategies = request.json.get('selected_strategies')
    
    # Call controller function to handle logic
    response_data = identify_weaknesses_controller(updated_fact_combination, selected_strategies)
    
    # Format response data for frontend, encapsulating each strategy's response
    formatted_response = {strategy: data for strategy, data in response_data.items()}
    
    # Return response to frontend
    return jsonify(formatted_response)

@app.route('/game/conclusion', methods=['POST'])
def conclusion():
    # Receive narrative details from the frontend
    data = request.get_json()
    narrative = data.get('narrative')
    strategy = data.get('strategy')
    
    # Call the controller function to process the data and generate a conclusion
    response_data = conclusion_controller(narrative, strategy)
    
    # Return the generated conclusion data to the frontend
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
