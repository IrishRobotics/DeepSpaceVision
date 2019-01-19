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

# read image from file (files are in subdirectory 2019VisionImages)
#img = cv2.imread('2019VisionImages\\RocketPanelStraightDark24in.jpg', cv2.IMREAD_COLOR)
img = cv2.imread('2019VisionImages\\RocketPanelStraightDark96in.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('2019VisionImages\\RocketPanelAngleDark60in.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('2019VisionImages\\RocketPanelStraight48in.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('2019VisionImages\\CargoSideStraightDark36in.jpg', cv2.IMREAD_COLOR)
cv2.imshow('Original Image', img)

# Convert Image to HSV
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Remove All color outside our green threshold tests
# (experimentally found using multi-image.py and gui.py from https://github.com/rr1706/Multi-Thresh)
imgGreenBW = cv2.inRange(imgHSV, np.array([60, 60, 180]), np.array([180, 255, 255]))
cv2.imshow('Image Green', imgGreenBW)

# TODO - May need more cleanup of images using techinques found in https://frc-pdr.readthedocs.io/en/latest/vision/contours.html

# Convert BW to BGR to Find Contours
imgGreenBGR = cv2.cvtColor(imgGreenBW, cv2.COLOR_GRAY2BGR)
img2, contours, hierarchy = cv2.findContours(imgGreenBW,  cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Remove contours smaller than 60 pixel area to eliminate far off things
minArea = 60

adjCoutours = []
for contour in contours:
    contourArea = cv2.contourArea(contour)
    #print (contourArea)
    if contourArea > minArea:
            adjCoutours.append(contour)

# Draw Coutours onto image for debugging in fuchsia as 3 pixel wide borders
for contour in adjCoutours:
    cv2.drawContours(imgGreenBGR, [contour], 0, (255, 0, 255), 3)

# Finding center of Coutours, draw center as 3 pixel wide 3 pixel thick circle in blue
points = []
for contour in adjCoutours:
    moments = cv2.moments(contour)
    centerX = int(moments['m10']/moments['m00'])
    centerY = int(moments['m01']/moments['m00'])
    pt = (centerX, centerY)
    cv2.circle(imgGreenBGR, pt, 3, (255, 0, 0), 3)
    points.append(pt)

# If we have 2 points find center
# TODO - We may find more than 2 points, might want to only return ones with biggest area which we calculated earlier
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

# Show final image
cv2.imshow('Final Image', imgGreenBGR)

# Wait for a key press and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows() 