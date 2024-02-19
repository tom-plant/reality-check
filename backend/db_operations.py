# db_operations.py
# AKA CRUD operations

from app import db
from models import User

def create_user(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user_password(user_id, new_password):
    user = User.query.get(user_id)
    user.password = new_password
    db.session.commit()

def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()