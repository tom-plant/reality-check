# app.py

from flask import Flask, session, jsonify, redirect, url_for, render_template, request, send_from_directory
from backend.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from flask_cors import CORS
from flask_session import Session 
import uuid
from dotenv import load_dotenv
import os
import sys
import logging

# Correctly placed imports
from backend.database import db, init_app
from backend.models import *
from backend.controllers import *
from backend.db_operations import *
from backend.routes import setup_routes

# Initialize Flask app in a factory function to avoid circular imports
def create_app():
    app = Flask(__name__, static_folder='build/static')

    # Session(app)
    load_dotenv()

    # Load environment configurations
    allowed_origins = os.getenv('ALLOWED_ORIGINS').split(',')
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": allowed_origins}})

    # Session settings
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_DOMAIN=".realitycheckgame.com",
        SESSION_COOKIE_SAMESITE='Lax'
    )

    # Set the configuration for SQLAlchemy directly after loading environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise Exception('SQLALCHEMY_DATABASE_URI is not set in the environment.')

    # Determine which environment to load and apply configurations
    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object(DevelopmentConfig)
    elif os.getenv('FLASK_ENV') == 'testing':
        app.config.from_object(TestingConfig)
    elif os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)  # Default to Config if not specified

    print('Configured Database URI:', app.config['SQLALCHEMY_DATABASE_URI'])

    # Import parts of the application that require a fully initialized app
    init_app(app)
    setup_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
