import numpy as np
import GripRunner
import Printing 
import config
import WebCam

def autocalibrate():
	print "Calibrating WebCam... (may not work)"
	exposure = WebCam.getExposure()
	numContours = 0
	while numContours != 2:
		image = WebCam.getImage()
		contours = GripRunner.run(image)
		numContours = len(contours)
		print numContours, exposure
		randomVar = np.random()
		if config.display:
			Printing.drawContours(image, contours)
			Printing.display(image)
		exposure = np.multiply(exposure, np.true_divide(2+randomVar, numContours+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
		WebCam.set(exposure=exposure)
	# get range of exposure


# 	shutter_speed = WebCam.getShutterSpeed()

# 		shutter_speed = np.multiply(shutter_speed, np.true_divide(numContours+randomVar, 2+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
# 		WebCam.set(shutter_speed=shutter_speed)
 
if __name__ == '__main__':
	autocalibrate()