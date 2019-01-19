# Make sure you install needed libraries as administator
# 1. numpy
#    pip install numpy
# 2. matplotlib
#    pip install matplotlib
# 3. OpenCV for python (cv2)
#    download opencv_python-3.4.5-cp37-cp37m-win32.whl from https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
#    cd to directory you downloaded the whl file to
#    pip install opencv_python-3.4.5-cp37-cp37m-win32.whl




import cv2
import numpy as np
import json
import time
import sys
from matplotlib import pyplot as plt
from cscore import CameraServer, VideoSource

# ------------------------------------------------------------------------------------
# Declare Global Variables
# ------------------------------------------------------------------------------------
configFile = "/boot/CameraConfig.json"


class CameraConfig: pass

team = None
server = False
cameraConfigs = []

# ------------------------------------------------------------------------------------
# Function: Report Parsing Error from File
# ------------------------------------------------------------------------------------
def parseError(str):
    print("config error in '" + configFile + "': " + str, file=sys.stderr)

# ------------------------------------------------------------------------------------
# Function: Read Single Camera Config
# ------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------
# Function: Read Config json File
# ------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------
# Function: Start Camera
# ------------------------------------------------------------------------------------
def startCamera(config):
    print("Starting camera '{}' on {}".format(config.name, config.path))
    camera = CameraServer.getInstance() \
        .getVideo(name=config.name)
        
    camera.setConfigJson(json.dumps(config.config))

    return camera

# read configuration
if not readConfig():
    sys.exit(1)

myCamera = startCamera(cameraConfigs[0])

#cap = cv2.VideoCapture(0)



#while(cap.isOpened()):
while(True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    ret, frame = myCamera.grabFrame(frame, 0.2)
    #if ret == True:
    if ret == 0:
        continue

    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    imgGreenBW = cv2.inRange(imgHSV, np.array([0, 0, 180]), np.array([60, 255, 255]))


    imgGreenBGR = cv2.cvtColor(imgGreenBW, cv2.COLOR_GRAY2BGR)
    img2, contours, hierarchy = cv2.findContours(imgGreenBW,  cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    minArea = 60

    adjCoutours = []
    for contour in contours:
        contourArea = cv2.contourArea(contour)
        #print (contourArea)
        if contourArea > minArea:
            adjCoutours.append(contour)

    for contour in adjCoutours:
        cv2.drawContours(imgGreenBGR, [contour], 0, (255, 0, 255), 3)

    points = []
    for contour in adjCoutours:
        moments = cv2.moments(contour)
        centerX = int(moments['m10']/moments['m00'])
        centerY = int(moments['m01']/moments['m00'])
        pt = (centerX, centerY)
        cv2.circle(imgGreenBGR, pt, 3, (255, 0, 0), 3)
        points.append(pt)

    # Display the resulting frame
    cv2.imshow('Frame', imgGreenBGR)
    cv2.imshow('Frame2',imgGreenBW )
    cv2.imshow('display',frame)
    cv2.imshow('displayConvtoHSV',imgHSV)
    
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 


# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows() 


