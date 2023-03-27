# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from flask import Flask
from flask.blueprints import Blueprint

from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import routes
import config

server  = Flask(__name__)

@server.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

SWAGGER_URL = '/thor-igot'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "THOR iGOT"
    }
)
server.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

if config.ENABLE_CORS:
    cors    = CORS(server, resources={r"*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.API_URL_PREFIX)

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
