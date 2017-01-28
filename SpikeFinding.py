import cv2
import numpy as np
from config import areaFromAFoot


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
	area = np.multiply(w,h)
	feetAway = np.sqrt(np.divide(areaFromAFoot, area))
	return center, feetAway
# Alternatively, use area of largest contour or area of bounding quadrilateral
