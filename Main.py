import cv2
import numpy as np
from ContourFinding import filterContours
from SpikeFinding import findCenter
import CameraLogic
import GripRunner

try:
	import NetworkTabling
except:
	if debug:
		print "no networktables"

pi = False
webcam = True

debug = True
adjustCoords = True

resolution = (640, 360)
exposure = 1
gripDoc = "grip.py"
sampleImage = "TestImages/GearTest.png"
#robust filtering and no editing
if adjustCoords:
	halfWidth = resolution[0]/2

if debug:
	from Printing import printResults

def main():
	if pi or webcam:
		camera = CameraLogic.initializeCamera(pi, webcam, resolution=resolution) # import and set exposure and resolution (or more)
		while True:
			image = CameraLogic.getImage()
			runVision(image)
	else:
		image = CameraLogic.getSampleImage(sampleImage)
		runVision(image)

def runVision(image):
	contours = GripRunner.run(image)
	targets = filterContours(contours) # To be edited if the last filter is changed in case of algorithmic changes. 
	center = findCenter(targets) #if 2, join and find center, if 1, return val, if 0 return input. if adjustCoords:	center[0] -= halfWidth
	if debug:
		printResults(image, contours, targets, center)

	try:
		networkTabling.publishToTables(center)
	except:
		pass

if __name__ == '__main__':
	main()
