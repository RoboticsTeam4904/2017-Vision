import cv2
import numpy as np
from config import *

# Convert to inches
nativeAngle = np.radians(57)
degPerPxl = np.divide(nativeAngle, resolution[1])

nativeAngleX = np.radians(90)
degPerPxlX = np.divide(nativeAngleX, resolution[0])

displacement = 0.5 # Vertical feet from camera to bottom of vision target
size = np.true_divide(5,12) # Height of target in feet
k = 1
cameraTilt = 0

width = np.divide(8.25, 12) #from centers. targets are 2x5 inches and 6.25 inches apart
middleY = np.true_divide(resolution[1], 2)
middleX = np.true_divide(resolution[0], 2)

def findCenter(contours):
	if len(contours) == 0:
		return False
	contour = np.concatenate(contours)
	x,y,w,h = cv2.boundingRect(contour)
	return (x + w/2, y + h/2)

def findCenterandDist(contours):
	numContours = len(contours)
	if numContours == 0:
		print "no contours"
		return False, 0
	contour = np.concatenate(contours)
	x,y,w,h = cv2.boundingRect(contour)
	center = (int(np.add(x, np.divide(w,2))), int(np.add(y, np.true_divide(h,2))))
	if numContours == 2:
		x1,y1,w1,h1 = cv2.boundingRect(contours[0])
		x2,y2,w2,h2 = cv2.boundingRect(contours[1])
		d1, d2 = distanceFromHeight(y1), distanceFromHeight(y2)
		if x1 > x2:
			d1, d2 = d2, d1

		distance = trueDistance(d1, d2)
		phi = angle(distance, d2)
		angleToGoal = np.multiply(degPerPxlX, np.subtract(middleX, y))

		robotAngle = phi + angleToGoal
		x, y = distance * np.cos(phi), distance * np.sin(phi)
		print x, y, robotAngle

		# print np.degrees(phi - np.pi/2), "ANGLE OFF IN DEGREES"
	else:
		distance = distanceFromHeight(y)
		print distance
	return center, distance * k

def distanceFromHeight(y):
	degrees = np.multiply(degPerPxl, np.subtract(middleY, y))
	degrees += cameraTilt
	distance = np.divide(np.add(displacement, size), np.tan(degrees)) # = displacement * cot(degreesFromMiddleToBottom)
	return distance

def trueDistance(d1, d2):
	squares = np.add(np.square(d1), np.square(d2))
	squared = np.subtract(np.multiply(2, squares), np.square(width))
	# print squared, "not negative?" #SHOULDN"T BE NEGATIVE IF CAMERA MOUNTED PROPERLY AND CONSTANTS CORRECTLY LABELED
	d = np.divide(np.sqrt(squared), 2)
	return d
	# d = 1/2 * sqrt(2*(d1^2+d2^2)-w^2)

def angle(d, d2):
	squares = np.subtract(np.add(np.true_divide(np.square(width), 4), np.square(d)), np.square(d2))
	# print d, np.divide(squares, np.multiply(width, d))
	phi = np.arccos(np.divide(squares, np.multiply(width, d)))
	# print phi
	return np.subtract(np.pi, phi)
	# angle = pi - acos(1/4*w^2 + d^2 - d2^2 / wd)


# def widthFromData(d1, d2, pxlsBetween):
# 	theta = np.multiply(pxlsBetween, degPerPxlX)
# 	sqaures = np.add(np.square(d1), np.square(d2))
# 	cos = np.multiply(2, np.multiply(d1, np.multiply(d2, np.cos(theta))))
# 	width = np.sqrt(np.subtract(squares, cos))
# 	return width

# def distanceFromAngle(d1,d2,theta):
# 	width = widthFromData(d1, d2, theta)
# 	return trueDistance(d1, d2, width)


def testFromAFoot(contours):
	center, feetAway = findCenterandDist(contours)
	global k
	k = np.true_divide(k, feetAway)


def largest(contours):
	areas = [cv2.contourArea(contour) for contour in contours]
	largest = np.amax(areas)
	return contours[areas.index(largest)]
