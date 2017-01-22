def initializeCamera(pi, webcam, resolution=(640,360)):
	if pi:
		from PiCamera import getImage, setCamera

	elif webcam:
		global getImage
		from WebCam import getImage, setCamera
		

def getSampleImage(sampleImage):
	import cv2
	return cv2.imread(sampleImage)
