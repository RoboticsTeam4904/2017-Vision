import cv2

def initializeCamera(pi, webcam, resolution=(640,360)):
	if pi:
		from PiCamera import initializeCamera, getImage, setCamera

	elif webcam:
		global getImage
		from WebCam import initializeCamera, getImage, setCamera

	if pi or webcam:
		initializeCamera(resolution=resolution)
		# getImage
	else:
		import cv2
	

def getTheImage(pi, webcam, sampleImage):
	if pi or webcam:
		return getImage()
	else:
		return getSampleImage(sampleImage)


def getSampleImage(sampleImage):
	# import cv2
	return cv2.imread(sampleImage)
