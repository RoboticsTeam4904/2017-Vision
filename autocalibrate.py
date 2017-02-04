import numpy as np
import GripRunner, Printing, WebCam
from config import debug, display, resolution
import cv2, time

minExposure = 5
maxExposure = 100
resolutionArea = np.multiply(resolution[0], resolution[1])
maxArea = np.divide(resolutionArea, 4)

targetAverage = 30
averageThreshold = 20

numTests = 5
maxBrightnessIterations = 20


def autocalibrate():
	# displace()
	exposure = WebCam.getExposure()
	if debug:
		b = time.clock()

	for iteration in xrange(maxBrightnessIterations):
		image = WebCam.getImage()
		if display:
			Printing.display(image)

		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		value = cv2.split(image)[2]
		average = cv2.mean(value)[0]
		if np.absolute(np.subtract(average, targetAverage)) < averageThreshold:
			if debug:
				print i, "num iterations, brightness lowering"
			break

		scaleBy = np.divide(targetAverage, average)
		newExposure = np.minimum(np.maximum(np.multiply(exposure, scaleBy), minExposure), maxExposure)
		if exposure == newExposure == minExposure:
			break
		exposure = newExposure
		WebCam.set(exposure=exposure)
	if debug:
		print "bright", time.clock() - b

	numGoodFrames = 0
	if debug:
		s = time.clock()
	for i in range(1000):
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		numContours = len(contours)
#		print numContours, exposure, WebCam.getExposure()
		if i%50 == 0:
			print "iteration #", i, "  Number of contours seen: ", numContours
		if numContours != 0:
			if tooLarge(contours):
				exposure = np.divide(exposure, 10)
		if numContours == 2:
			numGoodFrames += 1
			if numGoodFrames == numTests:
				if debug:
					print i, "num iterations grip"
					print "Finished grip succesfully", time.clock() - s
				return True
		else:
			numGoodFrames = 0
		randomVar = np.random.random_sample()
		scaleBy = np.true_divide(2+randomVar, numContours+randomVar)
		exposure = np.minimum(np.maximum(np.multiply(exposure, scaleBy), minExposure), maxExposure)
		WebCam.set(exposure=exposure)
		if display:
			Printing.drawContours(image, contours)
			Printing.display(image)
	if debug: 
		print "Failed grip", time.clock() - s
	return False


def tooLarge(contours):
	areas = [cv2.contourArea(contour, False) for contour in contours]
	largest = np.amax(areas)
	if largest > maxArea:
		return True
	else:
		return False

def displace():
	WebCam.set(exposure=2000)


if __name__ == '__main__':
	start = time.clock()
	autocalibrate()
	exposure = WebCam.getExposure()
	print time.clock() - start, "TOTAL TIME"

	while display:
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		Printing.drawContours(image, contours)
		Printing.display(image)
		cv2.waitKey(20)

# Get average value at the end of test to recalibrate targetAverage
	# image = cv2.imread('TestImages/Cancer.jpg')
	# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	# value = cv2.split(image)[2]
	# # value = np.array([image[:,:,2]])
	# average = cv2.mean(value)
	# print average