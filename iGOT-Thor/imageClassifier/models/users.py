# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

######################################################
# PROJECT : Image Profanity Classifier
# AUTHOR  : Tarento Technologies
# DATE    : Jan 22, 2020
######################################################


import io
import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
from common.errors import RestAPIError


'''
---------------------------------------
VARIABLES
---------------------------------------
'''
ERROR_MSG = "Something went Wrong!"

MODEL_PATH = 'imageClassifier/model.hdf5'
IMAGE_DEPTH = 3
IMAGE_WIDTH = 192
IMAGE_HEIGHT = 192
IMAGE_SHAPE = (IMAGE_DEPTH, IMAGE_HEIGHT, IMAGE_WIDTH)

if K.image_data_format() == 'channels_last':
    IMAGE_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_DEPTH)


'''
---------------------------------------
CLASSIFIER MODEL LOADING & LABELING
---------------------------------------
'''

model = load_model(MODEL_PATH)
labels = ['nsfw-nude', 'nsfw-risque', 'nsfw-sex', 'nsfw-violence', 'sfw']


# ######################################
# Image Preparation
# ######################################

def prepare_image(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    return img_tensor

import logging

logging.basicConfig(filename='error.log', filemode='a')
# ######################################
# Image Classification
# ######################################

def process(path):
    data = { "code" : 200,"success": False, "payload": {"image_profanity" : {},"classification" : "Offensive"}}
    try:
        img = Image.open(path)
        img_tensor = prepare_image(img)
        pred_prob = model.predict(img_tensor)
        # print(pred_prob)
        for index, prob in enumerate(pred_prob[0]):
            data["payload"]["image_profanity"][labels[index]] = round(float(prob),2)
        data["success"] = True
        data["payload"]["image_profanity"]["is_safe"] = bool(pred_prob[0][4] > 0.4)
        if data["payload"]["image_profanity"]["is_safe"] is True:
            data["payload"]["classification"] = "Not Offensive"
        return data
    except Exception as e_except:
        logging.error(e_except)
        return RestAPIError.internal_server_error()

class ICFModel():

    @staticmethod
    def upload_image1(img):
        try:
            img = io.BytesIO(img)
        except Exception as e_except:
            logging.error(e_except)
            return RestAPIError.internal_server_error()
        return process(img)
