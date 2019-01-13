import cv2
import numpy as np
from matplotlib import pyplot as plt 

# read image from file
img = cv2.imread('2019VisionImages\\RocketPanelStraightDark24in.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('2019VisionImages\\RocketPanelStraightDark96in.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('2019VisionImages\\RocketPanelStraight48in.jpg', cv2.IMREAD_COLOR)
cv2.imshow('Original Image', img)

img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# read image from camera 
#cap = cv2.VideoCapture(0)
#ret,  img = cap.read()

# removes pixes below a color value
#ret, dst = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)

dst = cv2.inRange(img2, np.array([60, 60, 180]), np.array([180, 255, 255]))
cv2.imshow('Processed Image', dst)

# makes image thinner
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
#erosion = cv2.erode(dst, kernel, iterations=1)
#cv2.imshow('Altered Image', erosion)

# makes image thicker
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
#dilation = cv2.dilate(dst, kernel, iterations=1)
#cv2.imshow('Altered Image', dilation)

# remote noise / artifacts
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
iopen = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
cv2.imshow('Altered Image', iopen)

# fills small holes
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
iclose = cv2.morphologyEx(iopen, cv2.MORPH_CLOSE, kernel2)

# Find outlines
# kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
# igrad = cv2.morphologyEx(iclose, cv2.MORPH_GRADIENT, kernel3)
# cv2.imshow('Altered Image 3', igrad)



cv2.waitKey(0)
cv2.destroyAllWindows() 