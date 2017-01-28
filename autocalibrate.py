import numpy as np
import GripRunner
import Printing 
import config
import WebCam
import cv2

minimumExposure = 3
maximumExposure = 1000
resolutionArea = 600000
maxArea = resolutionArea/4
# test image max area is 58106.0

def autocalibrate():
	print "Calibrating WebCam... (may not work)"
	exposure = WebCam.getExposure()
	numContours = 0
	while numContours != 2:
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		numContours = len(contours)
		print numContours, exposure, WebCam.getExposure()
		randomVar = np.random.random_sample()
		if config.display:
			Printing.drawContours(image, contours)
			Printing.display(image)
		exposure = np.multiply(exposure, np.true_divide(2+randomVar, numContours+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
		if tooLarge(contours):
			exposure = np.multiply(exposure, 0.1)
		exposure = np.min(np.max(exposure, minExposure), maxExposure)
		WebCam.set(exposure=exposure)
	# get range of exposure
	Printing.save(image, name="autocalibrate")

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
 
if __name__ == '__main__':
	autocalibrate()