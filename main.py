import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit
# from flask_socketio import SocketIO

from app import create_app, db, socketio
from app.config import config_dict


 
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # load configuration using default values 
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production]')

app = create_app(app_config)
# socketio = SocketIO(app)
Migrate(app, db)

print("Starting Flask App...")
if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    # app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )


if __name__ == '__main__':
    # app.run()
    socketio.run(app, debug=DEBUG, host='0.0.0.0', port=5000)
    