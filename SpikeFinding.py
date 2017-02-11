import cv2
import numpy as np
import config

def findSpike(contours): # returns isVisible, angleToGoal, distance
	isVisible=False
	numContours = len(contours)
	if numContours == 0:
		print "no contours"
		return False, 0, 0
	contour = np.concatenate(contours)
	X,Y,W,H = cv2.boundingRect(contour)
	center = (np.add(X, np.divide(W,2)), np.add(Y, np.true_divide(H,2)))
	angleToGoal = np.multiply(config.degPerPxl, np.subtract(np.true_divide(config.resolution[0], 2), center[0]))
	if numContours == 2:
		isVisible = True
		x1,y1,w1,h1 = cv2.boundingRect(contours[0])
		x2,y2,w2,h2 = cv2.boundingRect(contours[1])
		d1, d2 = distanceFromHeight(y1), distanceFromHeight(y2)
		if x1 > x2:
			d1, d2 = d2, d1
		distance = trueDistance(d1, d2)
		phi = angle(distance, d2)
		robotAngle = np.add(phi, angleToGoal)
		x, y = np.multiply(distance, np.cos(phi)), np.multiply(distance, np.sin(phi))
		if config.debug:
			print "distance                      ", distance, distanceFromHeight(Y)
			print "x,y,angle     ", x, y, np.degrees(angleToGoal)
	else:
		distance = distanceFromHeight(Y)
	return isVisible, np.degrees(angleToGoal), distance

def distanceFromHeight(y):
	degrees = np.multiply(config.degPerPxl, np.subtract(np.true_divide(config.resolution[1], 2), y))
	degrees = np.add(degrees, config.cameraTilt)
	distance = np.divide(config.displacement, np.tan(degrees))
	return distance

def trueDistance(d1, d2):
	squares = np.add(np.square(d1), np.square(d2))
	squared = np.subtract(np.multiply(2, squares), np.square(config.width))
	# print squared, "not negative?" #SHOULDN"T BE NEGATIVE IF CAMERA MOUNTED PROPERLY AND CONSTANTS CORRECTLY LABELED
	d = np.divide(np.sqrt(squared), 2)
	return d
	# d = 1/2 * sqrt(2*(d1^2+d2^2)-w^2)

def angle(d, d2):
	squares = np.subtract(np.add(np.true_divide(np.square(config.width), 4), np.square(d)), np.square(d2))
	phi = np.arccos(np.divide(squares, np.multiply(config.width, d)))
	return np.subtract(np.pi, phi)
	# angle = pi - acos(1/4*w^2 + d^2 - d2^2 / wd)


# def widthFromData(d1, d2, pxlsBetween):
# 	theta = np.multiply(pxlsBetween, config.degPerPxl)
# 	sqaures = np.add(np.square(d1), np.square(d2))
# 	cos = np.multiply(2, np.multiply(d1, np.multiply(d2, np.cos(theta))))
# 	config.width = np.sqrt(np.subtract(squares, cos))
# 	return config.width

# def distanceFromAngle(d1,d2,theta):
# 	config.width = widthFromData(d1, d2, theta)
# 	return trueDistance(d1, d2, config.width)