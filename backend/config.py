#config.py
import os

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

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_SQLALCHEMY_DATABASE_URI')
    API_KEY = os.environ.get('API_KEY')
    SQL_KEY = os.environ.get('SQL_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')  

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('JAWSDB_URL')
    API_KEY = os.environ.get('API_KEY')
    SQL_KEY = os.environ.get('SQL_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')  

# Automatically determine which config to load based on the environment
env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    CurrentConfig = ProductionConfig
elif env == 'testing':
    CurrentConfig = TestingConfig
else:
    CurrentConfig = DevelopmentConfig