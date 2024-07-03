# routes.py
from flask import jsonify, request, session, send_from_directory
from backend.controllers import * 
import logging


def setup_routes(app):

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory('build', 'index.html')

    @app.route('/debug/session')
    def debug_session():
        return jsonify(dict(session))

    @app.route('/')
    def hello():
        return "Hello, Dockerized Flask!"

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
        app.logger.debug(f"Request data: {request.json}")
        app.logger.debug(f"Session before processing: {dict(session)}")

        if 'user_data' not in session:
            app.logger.error("Session does not contain 'user_data'")
            return jsonify({"error": "User not logged in"}), 401
        
        # Receive selected actor and strategies from the frontend
        selected_actor = request.json.get('selected_actor')
        selected_strategies = request.json.get('selected_strategies')
        
        # Call the build_narrative_controller function to handle the logic
        response_data = build_narrative_controller(selected_actor, selected_strategies)
        
        app.logger.debug(f"Session after processing: {dict(session)}")
        # Return response to frontend
        return jsonify(response_data)

    @app.route('/game/select_news_article', methods=['POST'])
    def select_news_article():
        data = request.get_json()
        narrative = data['narrative']
        strategy = data['strategy']
        response_data = select_news_article_controller(narrative, strategy)
        return jsonify(response_data)

    @app.route('/game/select_instagram', methods=['POST'])
    def select_instagram():
        data = request.get_json()
        narrative = data['narrative']
        strategy = data['strategy']
        response_data = select_instagram_controller(narrative, strategy)
        return jsonify(response_data)

    @app.route('/game/select_youtube', methods=['POST'])
    def select_youtube():
        data = request.get_json()
        narrative = data['narrative']
        strategy = data['strategy']
        response_data = select_youtube_controller(narrative, strategy)
        return jsonify(response_data)

    @app.route('/game/select_shortform', methods=['POST'])
    def select_shortform():
        data = request.get_json()
        narrative = data['narrative']
        strategy = data['strategy']
        response_data = select_shortform_controller(narrative, strategy)
        return jsonify(response_data)

    @app.route('/game/set_primary_content', methods=['POST'])
    def set_primary_content():
        data = request.get_json()
        narrative = data['narrative']
        strategy = data['strategy']
        response_data = commit_primary_narrative_controller(narrative, strategy)
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
                
        # Return response to frontend
        return jsonify(response_data)

    @app.route('/game/conclusion', methods=['POST'])
    def conclusion():
        # Receive narrative details from the frontend
        data = request.get_json()
        narrative = data['narrative']
        strategy = data['strategy']
        
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
    
