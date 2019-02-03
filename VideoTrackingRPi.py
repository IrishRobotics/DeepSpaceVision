#!/usr/bin/env python3
'''Make sure you install needed libraries as administator
1. numpy
   pip install numpy
2. matplotlib
   pip install matplotlib
3. OpenCV for python (cv2)
   download opencv_python-3.4.5-cp37-cp37m-win32.whl from https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
   cd to directory you downloaded the whl file to
   pip install opencv_python-3.4.5-cp37-cp37m-win32.whl'''

import cv2
import numpy as np
import math
import pickle
import socket
import sys
import struct
import json
import time
import sys
import datetime
from cscore import CameraServer, VideoSource
from networktables import NetworkTablesInstance

#from matplotlib import pyplot as plt 
tnow = datetime.datetime.today()
print("Time Now {0}:{1}:{2}.{3}".format(tnow.hour, tnow.minute, tnow.second, tnow.microsecond))
print('Video Tracking DeepSpace:2606')

editorMode = False # False when running on Rpi 
sendContourProcessedImage  = True 
sendImageFrameRate = 30

Host = '192.168.1.114' # CHANGE THIS to roboRio Network Ip address
Port = 5804

sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Tcp Connection
sendSocket.connect((Host, Port))

class CameraConfig: pass
#cap = cv2.VideoCapture(0)


cameraConfigs = []

configFile = "/home/pi/cameraconfig.json"

def parseError(str):
    print("config error in '" + configFile + "': " + str, file=sys.stderr)

def readCameraConfig(config):
    cam = CameraConfig()

    # name
    try:
        cam.name = config["name"]
    except KeyError:
        parseError("could not read camera name")
        return False

    # path
    try:
        cam.path = config["path"]
    except KeyError:
        parseError("camera '{}': could not read path".format(cam.name))
        return False

    cam.config = config

    cameraConfigs.append(cam)
    return True



"""Read configuration file."""
def readConfig():
    global team
    global server

    # parse file
    try:
        with open(configFile, "rt") as f:
            j = json.load(f)
    except OSError as err:
        print("could not open '{}': {}".format(configFile, err), file=sys.stderr)
        return False

    # top level must be an object
    if not isinstance(j, dict):
        parseError("must be JSON object")
        return False

    # team number
    try:
        team = j["team"]
    except KeyError:
        parseError("could not read team number")
        return False

    # ntmode (optional)
    if "ntmode" in j:
        str = j["ntmode"]
        if str.lower() == "client":
            server = False
        elif str.lower() == "server":
            server = True
        else:
            parseError("could not understand ntmode value '{}'".format(str))

    # cameras
    try:
        cameras = j["cameras"]
    except KeyError:
        parseError("could not read cameras")
        return False
    for camera in cameras:
        if not readCameraConfig(camera):
            return False

    return True

# # Configure Camera
# # Main Settings
# cap.set(cv2.CAP_PROP_EXPOSURE, -12) # -8 is Around 6 ms exposure aparently
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
# cap.set(cv2.CAP_PROP_SATURATION,50)
# cap.set(cv2.CAP_PROP_CONTRAST,100)

# # FRAME rate/size
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap.set(cv2.CAP_PROP_FPS, 30)

# # AUTO setting SET TO OFF (DIFFRENT FOR EACH ONE)
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
# cap.set(cv2.CAP_PROP_AUTO_WB, 0)
# #cap.set(cv2.CAP_PROP_AUTOFOCUS, False)
# cap.set(cv2.CAP_PROP_BACKLIGHT, -1.0)

# # EXTRA SETTING TO PLAY WITH
# cap.set(cv2.CAP_PROP_SHARPNESS,0)
# #cap.set(cv2.CAP_PROP_GAIN, 0.0)

# read configuration

def startCamera(config):
    camera = CameraServer.getInstance().startAutomaticCapture(name=config.name, path=config.path)
    camera.setConfigJson(json.dumps(config.config))
    #CameraServer.getInstance().setConfigJson(json.dumps(config.config))
    camera = CameraServer.getInstance().getVideo()



    return camera

if not readConfig():
    sys.exit(1)
cap = startCamera(cameraConfigs[0])



#pictureCenter = (319.5,239.5)
pictureCenter = (159.5, 119.5)
focalLength = 713.582
exposureResetCounter = 0
imageSendCounter = 0

print('Camera has been configured: 640x480 30fps')

frame = np.zeros(shape = (240, 320, 3), dtype = np.uint8)

while(True):
  
  #exposureResetCounter = exposureResetCounter + 1
  #if exposureResetCounter == 29:
    #exposureResetCounter = 0
    #cap.set(cv2.CAP_PROP_EXPOSURE, -8) # -8 is Around 6 ms exposure aparently

  # Capture frame-by-frame
  #ret, frame = cap.read()
  time, frame = cap.grabFrame(frame)
  if time == 0:
      print(cap.getError())
      continue

  elif time > 0:
    tnow = datetime.datetime.today()

    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    imgGreenBW = cv2.inRange(imgHSV, np.array([30, 150, 40]), np.array([100, 255, 255]))


    imgGreenBGR = cv2.cvtColor(imgGreenBW, cv2.COLOR_GRAY2BGR)
    img2, contours, hierarchy = cv2.findContours(imgGreenBW,  cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    contoursSorted = sorted(contours,key=lambda x: cv2.contourArea(x), reverse = True)

    adjCoutours = []
    points = []

    if len(contoursSorted) >= 2:
        adjCoutours.append(contoursSorted[0])
        adjCoutours.append(contoursSorted[1])

    # minArea = 60


    # adjCoutours = []
    # for contour in contours:
    #     contourArea = cv2.contourArea(contour)
    #     #print (contourArea)
    #     if contourArea > minArea:
    #         adjCoutours.append(contour)

    


        if editorMode == True or sendContourProcessedImage == True: 
            for contour in adjCoutours:
                cv2.drawContours(imgGreenBGR, [contour], 0, (255, 0, 255), 3)

        for contour in adjCoutours:
            moments = cv2.moments(contour)
            moment0 = moments['m00']
            if moment0 != 0: 
                centerX = int(moments['m10']/moment0)
                centerY = int(moments['m01']/moment0)
                pt = (centerX, centerY)
                if editorMode == True: 
                    cv2.circle(imgGreenBGR, pt, 3, (255, 0, 0), 3)
                points.append(pt)


    if len(points) == 2:

        pt1 = points[1]
        pt2 = points[0]
        x = pt1[0] + ((pt2[0] - pt1[0]) / 2)
        y = pt1[1] + ((pt2[1] - pt1[1]) / 2)
        center = (int(x), int(y))

        # print points, draw as 3 pixel wide 3 pixel thick circle in red 
        if editorMode == True:   
            print( 'left point at {}'.format(pt1) )
            print( 'right point at {}'.format(pt2) )
            print( 'center is {}'.format(center))
        
        if editorMode == True or sendContourProcessedImage == True:
            cv2.circle(imgGreenBGR, center, 3, (0, 0, 255), 3)

        #Angle to Target
        targetRadian = math.atan((center[0]-pictureCenter[0])/focalLength)
        targetAngle = math.degrees(targetRadian)
        if editorMode == True: 
            print( 'angle is {}'.format(targetAngle))
        
        
        message = struct.pack('!iddhhhi', 1, targetAngle, 0.0, tnow.hour, tnow.minute, tnow.second, tnow.microsecond)
        sendSocket.send(message)

    else:
        message = struct.pack('!i', 2)
        sendSocket.send(message)

    if sendContourProcessedImage == True:
        imageSendCounter = imageSendCounter + 1
        if imageSendCounter >= sendImageFrameRate:
            imageSendCounter = 0
            result, data = cv2.imencode('.jpg ', imgGreenBGR)
            #result, data = cv2.imencode('.jpg ', frame)
            contourProcessedImageData = pickle.dumps(data, False)
            contourProcessedImageDataSize = len(contourProcessedImageData)
            message = struct.pack('!ii', 3, contourProcessedImageDataSize)
            print('Send image Size={}'.format(contourProcessedImageDataSize))
            sendSocket.send(message)
            sendSocket.sendall(contourProcessedImageData)

    if editorMode == True:    
        # Display the resulting frame
        cv2.imshow('Frame', imgGreenBGR)
        #Frame without centerpoints cv2.imshow('Frame2',imgGreenBW )
        cv2.imshow('display',frame)
        #cv2.imshow('displayConvtoHSV',imgHSV)

        
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
 
  # Break the loop
  else: 
    break
if editorMode == True:
    # Wait for a key press and close all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

