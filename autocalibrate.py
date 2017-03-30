import numpy as np

import GripRunner, Printing, WebCam
from config import debug, display, resolution
import cv2, time
from ContourFinding import *

minExposure = 1
maxExposure = 100
granularity = 2
resolutionArea = np.multiply(resolution[0], resolution[1])
maxArea = np.divide(resolutionArea, 4)

targetAverage = 30
averageThreshold = 10

numTests = 2
maxBrightnessIterations = 400



def calibrate():
	maxScore = 0
	maxScoreExposure = 0
	for exposure in range(minExposure, maxExposure, granularity):
		WebCam.set(exposure=exposure)
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		averageScore = filterContoursAutocalibrate(contours, image)
		if averageScore > maxScore:
			maxScore = averageScore
			maxScoreExposure = exposure
	WebCam.set(exposure=exposure)
	return True

def displace():
	WebCam.set(exposure=2000)


def test():
	displace()
	start = time.clock()
	calibrate()
	exposure = WebCam.getExposure()
	print time.clock() - start, "TOTAL TIME"

	while display:
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		Printing.drawContours(image, contours)
		Printing.display(image)
		cv2.waitKey(20)
