def initializeCamera(pi, webcam, resolution=(640,360)):
	if pi:
		from PiCamera import initializeCamera, getImage, setCamera

	elif webcam:
		from WebCam import initializeCamera, getImage, setCamera	

	if pi or webcam:
		initializeCamera(resolution=resolution)
	else:
		import cv2
	

def getTheImage():
	return getImage()


def getSampleImage(sampleImage):
	# import cv2
	return cv2.imread(sampleImage)
