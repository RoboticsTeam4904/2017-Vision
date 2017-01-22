def initializeCamera(pi, webcam, resolution=(640,360)):
	if pi:
		from PiCamera import initializeCamera, getImage, setCamera

	elif webcam:
		global getImage
		from WebCam import initializeCamera, getImage, setCamera

	initializeCamera(resolution=resolution)
		

def getSampleImage(sampleImage):
	import cv2
	return cv2.imread(sampleImage)
