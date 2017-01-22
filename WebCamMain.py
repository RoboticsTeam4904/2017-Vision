"""
Simple skeleton program for running an OpenCV Falsepeline generated by GRIP and using NetworkTables to send data.
Users need to:
1. Import the generated GRIP Falsepeline, which should be generated in the same directory as this file.
2. Set the network table server IP. This is usually the robots address (roborio-TEAM-frc.local) or localhost
3. Handle putting the generated code into NetworkTables
"""

import cv2
import numpy as np
from ContourFinding import filterContours
from SpikeFinding import findCenter
from NetworkTabling import publishToTables, initializeTables
import CameraLogic
from Printing import printResults
import GripRunner
from config import *


def main():
	GripRunner.initializeGrip(gripDoc, edited, withOpenCV3)

	camera = CameraLogic.initializeCamera(False, True, resolution) # import and set exposure and resolution (or more)

	try:
		network = initializeTables()
	except:
		network = None

	while True:
		runVision(camera, network) #count frame nums if necessary
	runVision(camera, network)


def runVision(camera, network):

	image = CameraLogic.getTheImage(False, True, sampleImage)
	contours = GripRunner.run(image)
	targets = filterContours(contours, debug) # To be edited if the last filter is changed in case of algorithmic changes. 
	center = findCenter(targets) #if 2, join and find center, if 1, return val, if 0 return input. if adjustCoords:	center[0] -= halfWidth
	if debug:
		printResults(image, contours, targets, center)
	try:
		publishToTables(debug, center, halfWidth)
	except:
		if debug:
			print "could not publish"

if __name__ == '__main__':
	main()
