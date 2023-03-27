from flask import Blueprint
from flask_restful import Api
from resources import UploadImage1


IMAGE_CLASSIFIER_BLUEPRINT = Blueprint("thor-igot", __name__)

Api(IMAGE_CLASSIFIER_BLUEPRINT).add_resource(
    UploadImage1, "/image/upload"
)
