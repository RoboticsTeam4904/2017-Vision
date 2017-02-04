import cv2
import numpy as np
from config import *

nativeAngle = 57
displacement = 0.5 # Vertical feet from camera to bottom of vision target
size = np.true_divide(5,12) # Height of target in feet
degPerPxl = resolution[1]/nativeAngle
k = 11
cameraTilt = 0

def findDistance(degPerPxl, pxlsFromCenter, size, disp):
	return ((size+disp)/np.tan(degPerPxl*pxlsFromCenter*np.pi/180))/12

def findCenter(contours):
	if len(contours) == 0:
		return False
	contour = np.concatenate(contours)
	x,y,w,h = cv2.boundingRect(contour)
	return (x + w/2, y + h/2)

def findCenterandDist(contours):
	if len(contours) == 0:
		return False, 0
	contour = np.concatenate(contours)
	x,y,w,h = cv2.boundingRect(contour)
	center = (int(np.add(x, np.divide(w,2))), int(np.add(y, np.true_divide(h,2))))

	largestContour = largest(contours)
	x,y,w,h = cv2.boundingRect(largestContour)
	degrees = degPerPxl * (resolution[1]/2-y)
	degrees += cameraTilt
	feetAway = np.divide((displacement + size), np.tan(degrees)) # = displacement * cot(degreesFromMiddleToBottom)
	# testFromAFoot(contours)
	# height = h*1944/1136.0
	# degrees = degPerPxl * h
	# # k = displacement from p?
	# feetAway = k * math.cot(degrees)
	# print "the height is", height
	# print h
	# #distanceInInches = -0.0075559*h*h + 3.3682*h - 346.59
	#distanceInInches = -0.41758*height + 125.43
	#feetAway = distanceInInches/12
	feetAway = (5.53096 * 5 * resolution[1])/(h * cameraHeight)/12
	print "height is ", h
	# #feetAway = np.sqrt(np.divide(heightFromAFoot, h))
	return center, feetAway * k
	# Maybe score contours based on size and position on screen

def testFromAFoot(contours):
	center, feetAway = findCenterandDist(contours)
	global k
	k = np.true_divide(k, feetAway)


def largest(contours):
	areas = [cv2.contourArea(contour) for contour in contours]
	largest = np.amax(areas)
	return contours[areas.index(largest)]
