import numpy as np
import GripRunner
import Printing 
import config
import WebCam
import cv2

minExposure = 3
maxExposure = 1000
resolutionArea = 600000
maxArea = resolutionArea/4
targetAverageValue = 50
averageValueThreshold = 30
numTests = 5
# test image max area is 58106.0

# image = cv2.imread('TestImages/Cancer.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# value = cv2.split(image)[2]
# # value = np.array([image[:,:,2]])
# average = cv2.mean(value)
# print average

def autocalibrate():
	print "Calibrating WebCam... (may not work)"
	exposure = WebCam.getExposure()
	for i in range(10):
		image = WebCam.getImage()
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		value = cv2.split(image)[2]
		average = cv2.mean(value)
		if config.display:
			Printing.display(image)
		if np.absolute(np.subtract(average, targetAverageValue)) < averageValueThreshold:
			break
		scaleBy = np.divide(targetAverageValue, average)
		exposure = np.minimum(np.maximum(np.multiply(exposure, scaleBy), minExposure), maxExposure)
		WebCam.set(exposure=exposure)

	numGoodFrames = 0
	for i in range(20):
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		numContours = len(contours)
		print numContours, exposure, WebCam.getExposure()
		if tooLarge(contours):
			exposure = np.divide(exposure, 10)
		if numContours == 2:
			numGoodFrames += 1
			if numGoodFrames == numTests:
				return True
		else:
			numGoodFrames = 0
		randomVar = np.random.random_sample()
		scaleBy = np.true_divide(2+randomVar, numContours+randomVar)
		exposure = np.minimum(np.maximum(np.multiply(exposure, scaleBy), minExposure), maxExposure)
		WebCam.set(exposure=exposure)
		if config.display:
			Printing.drawContours(image, contours)
			Printing.display(image)
	return false


def tooLarge(contours):
	areas = [cv2.contourArea(contour, False) for contour in contours]
	largest = np.amax(areas)
	if largest > maxArea:
		return True
	else:
		return False


# 	shutter_speed = WebCam.getShutterSpeed()

# 		shutter_speed = np.multiply(shutter_speed, np.true_divide(numContours+randomVar, 2+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
# 		WebCam.set(shutter_speed=shutter_speed)
 
# if numContours == 2:
# 			for i in range(numTests):
# 				image = WebCam.getImage()
# 				contours = GripRunner.run(image)
# 				numContours = len(contours)
# 				if numContours != 2:
# 					break
# 			else:
# 				break

# if __name__ == '__main__':
# 	autocalibrate()