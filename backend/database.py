# database.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy without an app
db = SQLAlchemy()

# Function to initialize the database with app
def init_app(app):
    db.init_app(app)
    migrate = Migrate(app, db)