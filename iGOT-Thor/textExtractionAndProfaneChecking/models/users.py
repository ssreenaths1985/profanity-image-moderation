# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
######################################################
# PROJECT : Text Extraction From Image &  
#           Text Profanity Checking
# AUTHOR  : Tarento Technologies
# DATE    : Jan 22, 2020
######################################################
import re

from textExtractionAndProfaneChecking.models.profanity import filter_and_tag
import keras_ocr
import logging
from common.errors import RestAPIError

logging.basicConfig(filename='error.log', filemode='a')
pipeline = keras_ocr.pipeline.Pipeline()

def process(image):
    input_string = ''
    try:
        images = [keras_ocr.tools.read(image)]
        prediction_groups = pipeline.recognize(images)
        for preds in prediction_groups:
            for pred in preds:
                print(pred[0])
                input_string = input_string +' '+ pred[0]
    except Exception as e_except:
        logging.error(e_except)
        return RestAPIError.internal_server_error()
    return input_string
class ICFModel():

    @staticmethod
    def upload_image1(image):
        data = {"code": 200, "payload": {}}
        try:
            input_string = process(image)
            if input_string:
                res = len(re.findall(r'\w+', input_string))
                if res < 20000:
                    text_result = filter_and_tag(input_string)
                    data["payload"].update(text_result)
                    return data
                else:
                    logging.error("Input Error: Word Count Exceeded!!")
                    return RestAPIError.word_limit()
        except Exception as e_except:
            logging.error(e_except)
            return RestAPIError.internal_server_error()

        return data
