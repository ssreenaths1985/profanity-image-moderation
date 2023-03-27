# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
######################################################
# PROJECT : India Map Detector
# AUTHOR  : Tarento Technologies
# DATE    : Jan 22, 2020
######################################################


import cv2
import os

from PIL import Image

from imageai.Detection.Custom import CustomObjectDetection
from indiaMapClassification.repositories import ICFRepositories
from common.errors import RestAPIError
from datetime import datetime

'''
---------------------------------------
DETECTION MODEL LOADING
---------------------------------------
'''


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("indiaMapDetection/model6.h5")
detector.setJsonPath("indiaMapDetection/detection_config.json")
detector.loadModel()



'''
---------------------------------------
VARIABLES
---------------------------------------
'''
detected = ''
cropped = ''
# detected = ''
# cropped = ''
# OUTPUT_PATH = "indiaMapDetection/image123/"+detected+".png"
# OUTPUT_CROPPED = "indiaMapDetection/image123/"+cropped+".png"
ERROR_MSG = "Something went Wrong!"

import logging

logging.basicConfig(filename='error.log', filemode='a')

# ######################################
# Detection process
# ######################################

def process(path):
    global detected
    global cropped
    try:
        data = {"Status": "Success",
                "code": 200,
                "payload": {"india_classification": []}}
        try:
            detected = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            detections = detector.detectObjectsFromImage(input_type="array",
                                                        input_image=path,
                                                        output_image_path="indiaMapDetection/image123/detected-"+detected+".png")
        except Exception as e_except:
            logging.error(e_except)
            return RestAPIError.internal_server_error()
        im_open = Image.open("indiaMapDetection/image123/detected-"+detected+".png")
        width, height = im_open.size
        if detections:
            count = 1
            temp = False
            temp1 = []
            for detection in detections:
                if detection["name"] == 'india':
                    count = count+1
                    temp = True
                    crop_width = detection["box_points"][2] - detection["box_points"][0]
                    crop_height = detection["box_points"][3] - detection["box_points"][1]
                    boundbox_new = box(detection["box_points"],
                                    crop_width, crop_height, height, width)
                    x_1 = int(boundbox_new[0])
                    y_1 = int(boundbox_new[1])
                    x_2 = int(boundbox_new[2])
                    y_2 = int(boundbox_new[3])
                    image = cv2.imread("indiaMapDetection/image123/detected-"+detected+".png")
                    roi = image[y_1:y_2, x_1:x_2]
                    cropped = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                    cv2.imwrite("indiaMapDetection/image123/detected-"+cropped+".png", roi)
                    try:
                        res = ICFRepositories.classify_image("indiaMapDetection/image123/detected-"+cropped+".png")
                    except Exception as e_except:
                        logging.error(e_except)
                        return RestAPIError.internal_server_error()
                    if os.path.exists("./indiaMapDetection/image123/detected-"+cropped+".png"):
                        os.remove("./indiaMapDetection/image123/detected-"+cropped+".png")
                    detection_classification = {"present": "true",
                                    "percentage_probability": detection["percentage_probability"],
                                                "classification": res}
                    temp1.append(detection_classification)
                    data["payload"].update({"india_classification": temp1})
            if not temp:
                data = {"Status": "Success",
                        "code": 200,
                        "payload": {"india_classification": []}}
                return data
            return data
        data = {"Status": "Success",
                "code": 200,
                "payload": {"india_classification": []}}
        return data
    except Exception as e_except:
        logging.error(e_except)
        return RestAPIError.internal_server_error()
# ######################################
# Increasing bounding box
# ######################################

def box(detection, crop_width, crop_height, height, width):
    # print(detection[1])
    try:
        crop_width = crop_width*0.05
        crop_height = crop_height*0.05
        # box(detection["box_points"])
        if (detection[0]-crop_width) >= 0:
            detection[0] = detection[0]-crop_width
        else:
            i = crop_width-5
            while (detection[0]-i) < 0:
                i = i-5
            if i > 0:
                detection[0] = detection[0]-i
        if (detection[1]-crop_height) >= 0:
            detection[1] = detection[1]-crop_height
        else:
            i = crop_height-5
            while (detection[1]-i) < 0:
                i = i-5
            if i > 0:
                detection[1] = detection[1]-i
        if (detection[2]+crop_width) <= width:
            detection[2] = detection[2]+crop_width
        else:
            i = crop_width-5
            while (detection[2]+i) > width:
                i = i-5
            if i > 0:
                detection[2] = detection[2]+i
        if (detection[3]+crop_height) <= height:
            detection[3] = detection[3]+crop_height
        else:
            i = crop_height - 5
            while (detection[3]+i) > height:
                i = i-5
            if i > 0:
                detection[3] = detection[3]+i
    except Exception as e_except:
        logging.error(e_except)
        return RestAPIError.internal_server_error()
    return detection


class ICFModel():
    

    @staticmethod
    def upload_image1(image):
        
        global detected
        result = process(image)
        

        if os.path.exists("./indiaMapDetection/image123/detected-"+detected+".png"):
            os.remove("./indiaMapDetection/image123/detected-"+detected+".png")
        return result
