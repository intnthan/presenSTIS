import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    
def register_blueprints(app):
    for module_name in (['authentication', 'model', 'perkuliahan']):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

# kode untuk configure database 
def configure_database(app):
    @app.before_request
    def initialize_database():
        try: 
            db.create_all()
            
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql+pymysql://' + os.path.join(basedir, 'presensi')

            print('> allback to MySQL with PyMySQL ')
            db.create_all()
    
    with app.app_context():
        db.create_all()
        
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    from .routes import routes
    app.register_blueprint(routes , url_prefix='/')
    bcrypt = Bcrypt(app)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    
    return app