import numpy as np
import config, GripRunner, Printing, WebCam, ContourFinding

minExposure = 3
maxExposure = 100
granularity = 2

def calibrate():
	maxScore, maxScoreExposure = 0, 0
	if config.debug:
		print "Checking exposures between {} and {} by incrementing by {}".format(minExposure, maxExposure, granularity)
	for exposure in range(minExposure, maxExposure, granularity):
		WebCam.set(exposure=exposure)
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		if config.display:
			Printing.drawContours(image, contours)
			Printing.display(image)
		averageScore = ContourFinding.filterContoursAutocalibrate(contours, image)
		if averageScore > maxScore:
			maxScore = averageScore
			maxScoreExposure = exposure
	if config.debug:
		print "Determined best exposure to be {} with a score of {}".format(maxScoreExposure, maxScore)
	WebCam.set(exposure=maxScoreExposure)
	return True

def displace():
	WebCam.set(exposure=2000)

def test():
	import cv2, time
	if config.debug:
		"Testing autocalibrate"
	displace()
	start = time.clock()
	calibrate()
	print time.clock() - start, "TOTAL TIME"
	if config.debug:
		print "Autocalibrate set exposure to {}".format(WebCam.getExposure())
	while config.display:
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		Printing.drawContours(image, contours)
		Printing.display(image)
		cv2.waitKey(20)
