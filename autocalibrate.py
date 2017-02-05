import numpy as np

def autocalibrate(camera, grip):
	print "Calibrating camera... (may not work)"
	shutter_speed = camera.getShutterSpeed()
	numContours = 0
	while numContours != 2:
		image = camera.getImage()
		contours = grip.run(image)
		# filtered = filterContours(contours) #maybe skip this step?
		numContours = len(contours)
		randomVar = np.random()
		shutter_speed = np.multiply(shutter_speed, np.true_divide(numContours+randomVar, 2+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
		camera.set(shutter_speed=shutter_speed)
		# min and Max this, maybe make negative, depending on range


# def autocalibrate(camera, grip):
# 	print "Calibrating camera... (may not work)"
# 	exposure = camera.getExposure
# 	numContours = 0
# 	while numContours != 2:
# 		image = camera.getImage()
# 		contours = grip.run(image)
# 		# filtered = filterContours(contours) #maybe skip this step?
# 		numContours = len(contours)
# 		randomVar = np.random()
# 		exposure = np.multiply(exposure, np.true_divide(2+randomVar, numContours+randomVar)) #np.true_divide(sqrtTwo, np.sqrt(numContours)
# 		camera.set(exposure=exposure)
# 		# min and Max this, maybe make negative, depending on range

# def 
# camera.set(exposure=10)