from flask import Blueprint
# import cv2

blueprint = Blueprint(
    'perkuliahan_blueprint',
    __name__,
    url_prefix='/perkuliahan',
)

# camera = cv2.VideoCapture(0)