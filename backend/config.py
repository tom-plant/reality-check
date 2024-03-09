#config.py
import os

API_KEY = os.environ.get('API_KEY')  
SECRET_KEY = os.environ.get('SECRET_KEY')  
SQL_KEY = os.environ.get('SQL_KEY')  
TEST_SQL_KEY = os.environ.get('TEST_SQL_KEY')  

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    API_KEY = os.environ.get('API_KEY')
    SQL_KEY = os.environ.get('SQL_KEY')
    SESSION_TYPE = 'filesystem'  
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_THRESHOLD = 100  

class TestingConfig(Config):
    TESTING = True
    TEST_SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.environ.get('API_KEY')
    TEST_SQL_KEY = os.environ.get('TEST_SQL_KEY')