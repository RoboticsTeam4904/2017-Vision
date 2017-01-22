import cv2

def initializeCamera(pi, webcam, resolution=(640,360)):
	if pi:
		from PiCamera import getImage, setCamera

	elif webcam:
		global getImage
<<<<<<< HEAD
		from WebCam import getImage, setCamera
		
=======
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

>>>>>>> dab0b28b0a866cdccc9e764003b970d5ad7a82f5

def getSampleImage(sampleImage):
	# import cv2
	return cv2.imread(sampleImage)
