# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
######################################################
# PROJECT : India Map Classifier
# AUTHOR  : Tarento Technologies
# DATE    : Jan 22, 2020
######################################################


import tensorflow as tf
from tensorflow import keras
from common.errors import RestAPIError


'''
---------------------------------------
CLASSIFICATION MODEL LOADING
---------------------------------------
'''
from fastai.vision import *
from fastai.metrics import error_rate, accuracy

import warnings
warnings.filterwarnings('ignore')
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

import pickle
filename = dir_path+'1/fastai_model/finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

loaded_model = loaded_model.load(dir_path+'1/fastai_model/stage-2')
# model = keras.models.load_model('indiaMapClassification/models1/local/V1')

import logging

logging.basicConfig(filename='error.log', filemode='a')


# def infer_by_path(img):
#     try:
#         image = keras.preprocessing.image.load_img(img, target_size=(224, 224))
#         return infer_by_file(image)
#     except Exception as e_except:
#         logging.error(e_except)
#         return RestAPIError.internal_server_error()

# def infer_by_file(image):
#     try:
#         img_array = keras.preprocessing.image.img_to_array(image)
#         img_array = tf.expand_dims(img_array, 0)
#         predictions = model.predict(img_array)
#         score = tf.nn.softmax(predictions[0])
#         result = {'correct_percentage' : round(score[0].numpy()*100),
#                 'incorrect_percentage' : round(score[1].numpy()*100)}
#         return result
#     except Exception as e_except:
#         logging.error(e_except)
#         return RestAPIError.internal_server_error()



class ICFModel():

    @staticmethod
    def classify_image(image):
        result = {'correct_percentage' : 0,
                    'incorrect_percentage' : 0}
        try:
            cat, tensor, probs = loaded_model.predict(open_image(image))
            print(probs)
            if (probs[0] > probs[2]) and (probs[0] > probs[3]) and (probs[0] > probs[4]) :
                result = {'correct_percentage' : 100, 'incorrect_percentage' : 0}

            else:
                if (probs[1] > probs[2]) and (probs[1] > probs[3]) and (probs[1] > probs[4]):
                    result = {'correct_percentage' : 100, 'incorrect_percentage' : 0}
                else:
                    result = {'correct_percentage' : 0, 'incorrect_percentage' : 100}
    
        except Exception as e_except:
            logging.error(e_except)
            return RestAPIError.internal_server_error()

        return result
