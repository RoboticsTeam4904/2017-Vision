camera = None

def getImage():
	retval, image = camera.read()
	return image

def initializeCamera(resolution=(640,360)):
	import cv2
	camera = cv2.VideoCapture(0)
	setCamera(resolution=resolution)

def setCamera(resolution=False, exposure=False)
	if resolution:
		camera.set(3, resolution[0])
		camera.set(4, resolution[1])
	if exposure
		camera.set(15, 0.1) # exposure
	return camera
