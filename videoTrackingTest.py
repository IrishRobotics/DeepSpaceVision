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
from matplotlib import pyplot as plt 


cap = cv2.VideoCapture(0)
#Exposure
cap.set(15,0.1)
#Saturation
cap.set(12,40)
#Brightness
cap.set(10,0.1)
#Contrast
cap.set(11,0)


while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    imgGreenBW = cv2.inRange(imgHSV, np.array([60, 60, 180]), np.array([180, 255, 255]))


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
 
  # Break the loop
  else: 
    break

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows() 


