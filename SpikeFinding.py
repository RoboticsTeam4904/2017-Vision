import cv2
import numpy as np
from config import *


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

	height = 1.0*h/(1136.0/1944)
	print "the height is", height
	print h
	#distanceInInches = -0.0075559*h*h + 3.3682*h - 346.59
	distanceInInches = -0.41758*height + 125.43
	feetAway = distanceInInches/12
	#feetAway = (5.53096 * 5 * resolution[1])/(h * cameraHeight)/12 
	#feetAway = np.sqrt(np.divide(heightFromAFoot, h))
	return center, feetAway