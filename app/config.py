import os
import random
import string

class Config(object):
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    #  Assets management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')
    
    # set up secret key
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_letters) for i in range(32))
        
    DB_NAME     = os.getenv('DB_NAME', None)
    DB_ENGINE   = os.getenv('DB_ENGINE', None)
    DB_USERNAME = os.getenv('DB_USERNAME', None)
    DB_PASSWORD = os.getenv('DB_PASSWORD', None)
    DB_HOST     = os.getenv('DB_HOST', None)    
    DB_PORT     = os.getenv('DB_PORT', None)
    
    # try to set up database uri  
    if DB_ENGINE and DB_NAME and DB_USERNAME: 
        try:
            # relational DBMS: mysql 
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
            )
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SQLALCHEMY_RECORD_QUERIES = True
            USE_SQLITE = False
            
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e) )
            print('> Fallback to SQLite ')  
    
        
class ProductionConfig(Config):
    DEBUG = False
    
    # security 
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
    
class DebugConfig(Config):
    DEBUG = True

# load all config classes
config_dict ={
    'Production': ProductionConfig,
    'Debug': DebugConfig
}