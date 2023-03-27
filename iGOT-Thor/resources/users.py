# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import io
import logging
import numpy


from flask_restful import Resource
from imageClassifier.repositories import ICFRepositories
from indiaMapDetection.repositories import ICFRepositories1
from textExtractionAndProfaneChecking.repositories import ICFRepositories2
from common.errors import RestAPIError

import config
import flask
from PIL import Image
import keras_ocr
pipeline = keras_ocr.pipeline.Pipeline()
ERROR_MSG = "Something went Wrong!"



OCR = ""
MAP = ""
IMG_PROFANITY = ""
profanity_response = {}

logging.basicConfig(filename='error.log', filemode='a',
                            format='%(name)s - %(levelname)s - %(message)s')





def image_profanity(img):
    global profanity_response
    try:
        image_result = ICFRepositories.upload_image1(img)
    except Exception as e_except:
        logging.error(e_except)
        return RestAPIError.internal_server_error()
    if image_result["code"] == 200:
        profanity_response["payload"].update(image_result["payload"])
    else:
        return image_result
    return image_result





def map_detection(img):
    global profanity_response
    try:
        map_result = ICFRepositories1.upload_image1(numpy.asarray(img))
    except Exception as e_except:
        logging.error(e_except)
        return RestAPIError.internal_server_error()
    if map_result["code"] == 200:
        profanity_response["payload"].update(map_result["payload"])
    else:
        return map_result
    return map_result






def text_profanity(img):
    global profanity_response
    profanity_response["payload"].update({"text_profanity" : {}})
    try:
        text_result = ICFRepositories2.upload_image1(numpy.asarray(img))
        if text_result["code"] == 200:
            if text_result["payload"] != {}:
                key = "payload.classification"
                if key not in profanity_response:
                    profanity_response["payload"]["classification"] = 'Not Offensive'
                if text_result["payload"]["overall_text_classification"]["classification"] == 'Offensive':
                    profanity_response["payload"]["classification"] = 'Offensive'
                profanity_response["payload"]["text_profanity"] = text_result["payload"]
    except Exception as e_except:
        return text_result
    return text_result


class UploadImage1(Resource):


    def post(self):

        global OCR
        global MAP
        global IMG_PROFANITY
        global profanity_response

        OCR = config.ENABLE_OCR
        MAP = config.ENABLE_MAP
        IMG_PROFANITY = config.ENABLE_IMG_PROFANITY
        profanity_response = {"code": 200, "success": True, "payload": {}}

        if flask.request.files.get("image"):
            # txt = flask.request.values.get("ocr")

            if flask.request.values.get("ocr"):
                ocr = flask.request.values.get("ocr")
                if ocr == '1':
                    OCR = True
                elif ocr == '0':
                    OCR = False
                else :
                    logging.error('No Key or Value')
                    return RestAPIError.bad_request()
            if flask.request.values.get("map"):
                map = flask.request.values.get("map")
                if map == '1':
                    MAP = True
                elif map == '0':
                    MAP = False
                else :
                    logging.error('No Key or Value')
                    return RestAPIError.bad_request()
            if flask.request.values.get("img_prof"):
                img_prof = flask.request.values.get("img_prof")
                if img_prof == '1':
                    IMG_PROFANITY = True
                elif img_prof == '0':
                    IMG_PROFANITY = False
                else :
                    logging.error('No Key or Value')
                    return RestAPIError.bad_request()

            img = flask.request.files["image"].read()
            filename = flask.request.files["image"].filename
            file_type = filename.split(".")[-1]
            if file_type.lower() not in ["jpeg","png","jpg"]:
                logging.error('Image Not of Correct Format')
                return RestAPIError.bad_input()
        else:
            logging.error('No Key or Value')
            return RestAPIError.bad_request()

        try:
            # IMAGE PROFANITY
            if IMG_PROFANITY:
                image_result = image_profanity(img)
                if image_result["code"] != 200:
                    return flask.jsonify(image_result)


            try:
                img = Image.open(io.BytesIO(img)).convert('RGB')
            except Exception as e_except:
                logging.error(e_except)
                return RestAPIError.internal_server_error()
            if MAP:
                map_result = map_detection(img)
                if map_result["code"] != 200:
                    return flask.jsonify(map_result)
            if OCR:
                text_result = text_profanity(img)
                if text_result["code"] != 200:
                    return flask.jsonify(text_result)
            return flask.jsonify(profanity_response)
        except Exception as e_except:
            logging.error(e_except)
            return RestAPIError.internal_server_error()
    