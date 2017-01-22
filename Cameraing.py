import cv2

def initializeCamera(debug, pi, webcam):
	if pi:
		import camera
		camera.camera.resolution = resolution
		return camera

	elif webcam:
		camera = cv2.VideoCapture(0)
		camera.set(3, resolution[0])
		camera.set(4, resolution[1])
		# camera.set(15, 0.1) # exposure
		return camera

	else:
		return None

def getImage(camera, debug, webcam, pi, sampleImage):
	# retval, image = camera.read()
	if debug:
		print "Getting image..."

	if pi:
		return camera.getImage()

	elif webcam:
		retval, image = camera.read()
		return image

	else: #sample image
		return cv2.imread(sampleImage)
