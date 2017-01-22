import cv2
from PiCamera import initializePiCamera, getPiImage
from WebCam import initializeWebCamera, getWebCamImage

def initializeCamera(debug, pi, webcam, resolution):
	if pi:
		return initializePiCamera(resolution)

	elif webcam:
		return initializeWebCamera(resolution)

	else:
		return None

def getImage(camera, debug, webcam, pi, sampleImage):
	# retval, image = camera.read()
	if debug:
		print "Getting image..."

	if pi:
		return getPiImage(camera)

	elif webcam:
		return getWebCamImage(camera)

	else: #sample image
		return cv2.imread(sampleImage)
