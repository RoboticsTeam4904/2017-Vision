import numpy as np
import config, GripRunner, Printing, WebCam, ContourFinding

minExposure = 3
maxExposure = 100
granularity = 3

def calibrate():
	bestScore, bestExposure = 1000, minExposure
	if config.debug:
		print "Checking exposures between {} and {} by incrementing by {}".format(minExposure, maxExposure, granularity)
	for exposure in range(minExposure, maxExposure, granularity):
		WebCam.set(exposure=exposure)
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		if config.display:
			Printing.drawContours(image, contours)
			Printing.display(image)
		averageScore = ContourFinding.averageContourScore(contours, image)
		if averageScore < bestScore:
			bestScore, bestExposure = averageScore, exposure
	if config.debug:
		print "Determined best exposure to be {} with a score of {}".format(bestExposure, bestScore)
	WebCam.set(exposure=bestExposure)

def test():
	import cv2, time
	if config.debug:
		print "Testing autocalibration"
	WebCam.set(exposure=2000) # Displace camera's exposure
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
