"""
Simple skeleton program for running an OpenCV pipeline generated by GRIP and using NetworkTables to send data.
Users need to:
1. Import the generated GRIP pipeline, which should be generated in the same directory as this file.
2. Set the network table server IP. This is usually the robots address (roborio-TEAM-frc.local) or localhost
3. Handle putting the generated code into NetworkTables
"""

import cv2
import numpy as np
from ContourFinding import filterContours
from SpikeFinding import findCenter
from NetworkTabling import publishToTables, initializeTables
from Cameraing import getImage, initializeCamera
from Printing import printResults

pi = False
webcam = False

debug = True
continuous = True
edited = False
adjustCoords = True
withOpenCV3 = True

resolution = (640, 360)
exposure = 1
ip = "10.49.4.2"
team = 4904
gripDoc = "grip.py"
sampleImage = "TestImages/GearTest.png"

if adjustCoords:
	halfWidth = resolution[0]/2

if not pi and not webcam:
	continuous = False

def main():
	pipeline = initializeGrip(gripDoc)
	camera = initializeCamera(debug, pi, webcam) # import and set exposure and resolution (or more)
	try:
		network = initializeTables()
	except:
		network = None

	while continuous:
		runVision(camera, network, pipeline) #count frame nums if necessary
	runVision(camera, network, pipeline)

	# if continuous:
	# 	while True:
	# 		runVision(camera, network, pipeline) #count frame nums if necessary
	# else:
	# 	runVision(camera, network, pipeline)

def runVision(camera, network, pipeline):
	image = getImage(camera, debug, webcam, pi, sampleImage)
	pipeline.process(image)
	targets = filterContours(pipeline.filter_contours_output, debug) # To be edited if the last filter is changed in case of algorithmic changes. 
	center = findCenter(targets) #if 2, join and find center, if 1, return val, if 0 return input. if adjustCoords:	center[0] -= halfWidth
	if debug:
		printResults(pipeline.filter_contours_output, center, image)
	try:
		publishToTables(debug, network, center)
	except:
		if debug:
			print "could not publish"

def initializeGrip(doc):
	if not edited:
		import EditGeneratedGrip
		EditGeneratedGrip.editCode(doc, withOpenCV3=withOpenCV3)
	from grip import GripVisionPipeline  # TODO change the default module and class, if needed
	return GripVisionPipeline()

	# total_contour = np.concatenate((largest_contour, second_largest_contour))
		# x, y, w, h = cv2.boundingRect(total_contour) # Works best when camera is horizontal relative to target

		# center = (x+w/2, y+h/2)
		# if debug:
		# 	print "Found Center:", center
		# 	cv2.drawContours(image, contours, -1, (70,70,0), 3)
		# 	cv2.drawContours(image, [largest_contour], -1, (0,255,0), 3)
		# 	cv2.drawContours(image, [second_largest_contour], -1, (0,0,255), 3)
		# 	cv2.drawContours(image, [total_contour], -1, (255,0,0), 3)
		# 	cv2.circle(image, center, 4, (255, 255, 255))
		# 	cv2.imshow("Contours Found", image)
		# 	cv2.waitKey(0)
		# 	cv2.destroyAllWindows()
		# return center
	
	# 	x, y, w, h = cv2.boundingRect(contours[0])
	# 	center = (x+w/2, y+h/2)
	# 	if debug:
	# 		print "Found Center:", center
	# 		print "1 contour found (no bueno)"
	# 		cv2.drawContours(image, contours, -1, (70,70,0), 3)
	# 		cv2.circle(image, center, 4, (255, 255, 255))
	# 		cv2.imshow("Contours Found", image)
	# 		cv2.waitKey(0)
	# 		cv2.destroyAllWindows()
	# 	return center
	# else:
	# 	if debug:
	# 		print "RIP. no contours."
	# 	return (0,0)

	# if debug:
	# 	print "Got image. Analyzing image (pipeline process)..."
	# 	print "Image processed. Analyzing contours..."
	# 	print "Analyzed. Publishing to network tables..."

	
	

if __name__ == '__main__':
	main()
