import threading
from _thread import start_new_thread, exit_thread
import time
import client_utilities.ClientUtilities as client_utils
import socket
import sys
import io
import struct
import numpy as np
import argparse
import os
import traceback
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import scipy.io
import scipy.misc
import numpy as np
import pandas as pd
import time
import tensorflow as tf
from keras import backend as K
from keras.layers import Input, Lambda, Conv2D
from keras.models import load_model, Model
from ObjectDetection.yad2k.models.keras_yolo import yolo_head, yolo_boxes_to_corners, preprocess_true_boxes, yolo_loss, yolo_body
from ObjectDetection.PreprocessingRPi import ReadAnchors, ReadClasses, PreprocessImageHybrid, ScaleBoxes, GenerateColors, DrawBoxes
from ObjectDetection.Postprocessing import YoloEval, YoloFilterBoxes, YoloNonMaxSuppression
from ObjectDetection.ExceptionHandler import RetryError
from ObjectDetection.RPiMainUtilities import PredictNetwork, PredictNodeCam, ModelLoader
from ObjectDetection.FaceRecognitionUtilities import LoadDatabase, LoadFaceModel, SearchPerson, TripleLoss
from PIL import Image
from cv2 import cv2 as cv

def ServerVideo(ObjectDetectionUtils:tuple, host = "127.0.0.1", port = 8000):
    '''
    Function to start a video server at given host ip and port

    Arguments:
        ObjectDetectionUtils {tuple} -- All of necessary utils for object detection
    
    Keyword Arguments:
        host {str} -- The host ip address to start the video server (default: {"127.0.0.1"})
        port {int} -- The port to start the video server (default: {8000})
    '''
    server_socket = socket.socket()
    print("[INFO] Video Server Socket Created")
    server_socket.bind((host, port))
    print("[INFO] Video Server binded")

    sess, yoloModel, FRmodel, database, classNames, scores, boxes, classes = ObjectDetectionUtils
    server_socket.listen(0)
    print("[INFO] Listening for incoming video feed")

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        while True:
            # Exiting mechanism
            if cv.waitKey(1) & 0xFF == ord('q'):
                raise KeyboardInterrupt
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            cv2image = PredictNetwork(sess, yoloModel, FRmodel, database, image, classNames, scores, boxes, classes)
            cv.imshow("output", cv2image)
            # print('Image is %dx%d' % image.size)
            # image.verify()
            # print('Image is verified')
            # img = cv.imread()

    except Exception as err:
        print("{ERROR}: ", err)
        connection.close()
        server_socket.close()
        exit(1)

    finally:
        connection.close()
        server_socket.close()
        return True


if __name__ == "__main__":

    localhost = "127.0.0.1"
    port = 8000
    if len(sys.argv) == 3:
        localhost = sys.argv[1]
        port = int(sys.argv[2])
    # Getting a session for Keras
    print("[+] Setting up Keras Session")
    try:
        sess = K.get_session()
    except Exception as err:
        print("[+] Session not acquired -- ERROR: ", err)
        traceback.print_exc()
        exit(1)
    
    # Getting Class Names and anchors
    classNames = ReadClasses("./ObjectDetection/model_data/coco_classes.txt")
    anchors = ReadAnchors("./ObjectDetection/model_data/yolo_anchors.txt")
    imageShape = (480. , 640.)
    

    # Loads the model
    while(True):
        yoloModel, status, retry = ModelLoader("ObjectDetection/model_data/yolo.h5")
        
        # check status and retry factors
        if status == False:
            if retry == False:
                print("[+] Quiting application after an exception")
                exit(1)
            else:
                print("[+] Reverting back to previous checkpoint")
                continue
        else:
            break
    
    print("[+] Model Loaded")
    print("[+] Setting up model")
    yoloOutputs = yolo_head(yoloModel.output, anchors, len(classNames))
    scores, boxes, classes = YoloEval(yoloOutputs, imageShape)
    

    FRmodel = None
    database = None #LoadDatabase("Database", FRmodel)
    print("[+] Database loaded")
    ObjectDetectionUtils = (sess, yoloModel, FRmodel, database, classNames, scores, boxes, classes)
    ServerVideo(ObjectDetectionUtils, localhost, port)