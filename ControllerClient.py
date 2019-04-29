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
from ObjectDetection.Preprocessing import ReadAnchors, ReadClasses, PreprocessImageHybrid, ScaleBoxes, GenerateColors, DrawBoxes
from ObjectDetection.Postprocessing import YoloEval, YoloFilterBoxes, YoloNonMaxSuppression
from ObjectDetection.ExceptionHandler import RetryError
from ObjectDetection.RPiMainUtilities import PredictNetwork, PredictNodeCam, ModelLoader
from ObjectDetection.FaceRecognitionUtilities import LoadDatabase, LoadFaceModel, SearchPerson, TripleLoss
from PIL import Image
from cv2 import cv2 as cv

# The Controller for the bot
def ControlClient(host = "127.0.0.1", port = 5000):
    '''
    Function to setup a client to control the server
    which would be the RPi bot
    
    Keyword Arguments:
        host {str} -- The server ip address to connect (default: {"127.0.0.1"})
        port {int} -- the server port address to connect (default: {5000})
    '''
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[INFO] Client side socket created")
    except socket.error as err:
        print("{ERROR}: Socket couldn't be created: ", err)
    
    except Exception as err:
        print("{CRITICAL}: uncaught error: ", err)
    
    # connect to server
    while True:
        try:
            clientSocket.connect((host, port))
            print("[INFO] Connected to RPi Bot")
            break
        except socket.error as err:
            print("[WARN] Connect error: ", err)
            print("[INFO] Trying after 5 seconds")
            time.sleep(5000)
            continue
        
        except Exception as err:
            print("{CRITICAL}: uncaught error: ", err)
            clientSocket.close()
            exit(1)
        
    # send controlling data
    while True:
        try:
            client_utils.clientSocket = clientSocket
            client_utils.ControlBot()
            raise KeyboardInterrupt
            
        except KeyboardInterrupt as err:
            print("[INFO] Shutting down Controller")
            break
        
        except Exception as err:
            print("{CRITICAL}: uncaught error: ", err)
            clientSocket.close()
            exit(1)
        
    clientSocket.close()
    return True

if __name__ == "__main__":
    
    localhost = "127.0.0.1"
    port = 5000
    if len(sys.argv) == 3:
        localhost = sys.argv[1]
        port = int(sys.argv[2])

    ControlClient(localhost, port)

    