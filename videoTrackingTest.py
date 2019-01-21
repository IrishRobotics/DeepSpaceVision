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
import math
from matplotlib import pyplot as plt 


cap = cv2.VideoCapture(0)
# Configure Camera
# Main Settings
cap.set(cv2.CAP_PROP_EXPOSURE, -8) # -8 is Around 6 ms exposure aparently
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
cap.set(cv2.CAP_PROP_SATURATION,50)
cap.set(cv2.CAP_PROP_CONTRAST,100)

# FRAME rate/size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# AUTO setting SET TO OFF (DIFFRENT FOR EACH ONE)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, False)
cap.set(cv2.CAP_PROP_BACKLIGHT, -1.0)

# EXTRA SETTING TO PLAY WITH
cap.set(cv2.CAP_PROP_SHARPNESS,0)
cap.set(cv2.CAP_PROP_GAIN, 0.0)

pictureCenter = (319.5,239.5)
focalLength = 713.582

while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    imgGreenBW = cv2.inRange(imgHSV, np.array([30, 150, 80]), np.array([100, 255, 255]))


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

    if len(points) == 2:

        pt1 = points[1]
        pt2 = points[0]
        x = pt1[0] + ((pt2[0] - pt1[0]) / 2)
        y = pt1[1] + ((pt2[1] - pt1[1]) / 2)
        center = (int(x), int(y))

        # print points, draw as 3 pixel wide 3 pixel thick circle in red 
        print( f'left point at {pt1}' )
        print( f'right point at {pt2}' )
        print( f'center is {center}')
        cv2.circle(imgGreenBGR, center, 3, (0, 0, 255), 3)

        #Angle to Target
        targetRadian = math.atan((center[0]-pictureCenter[0])/focalLength)
        targetAngle = math.degrees(targetRadian)
        print( f'angle is {targetAngle}')



    # Display the resulting frame
    cv2.imshow('Frame', imgGreenBGR)
    #Frame without centerpoints cv2.imshow('Frame2',imgGreenBW )
    cv2.imshow('display',frame)
    #cv2.imshow('displayConvtoHSV',imgHSV)

    #TODO REMEMBER TO REMOVE KEY PRESS AND SEND NETWORKTABLES HERE

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows() 


