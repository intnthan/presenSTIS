from flask import Blueprint

blueprint = Blueprint(
    'perkuliahan_blueprint',
    __name__,
    url_prefix='/perkuliahan',
)
