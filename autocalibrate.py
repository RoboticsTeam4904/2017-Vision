import numpy as np
import GripRunner

def autocalibrate(camera):
	print "Calibrating camera... (may not work)"
	exposure = camera.getExposure()
	numContours = 0
	while numContours != 2:
		image = camera.getImage()
		contours = GripRunner.run(image)
		numContours = len(contours)
		print numContours, exposure
		randomVar = np.random()
		exposure = np.multiply(exposure, np.true_divide(2+randomVar, numContours+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
		camera.set(exposure=exposure)
	# get range of exposure


# 	shutter_speed = camera.getShutterSpeed()

# 		shutter_speed = np.multiply(shutter_speed, np.true_divide(numContours+randomVar, 2+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
# 		camera.set(shutter_speed=shutter_speed)
