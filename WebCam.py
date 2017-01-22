def getWebCamImage(camera):
	retval, image = camera.read()
	return image

def initializeWebCamera(resolution):
	camera = cv2.VideoCapture(0)
	camera.set(3, resolution[0])
	camera.set(4, resolution[1])
	# camera.set(15, 0.1) # exposure
	return camera
