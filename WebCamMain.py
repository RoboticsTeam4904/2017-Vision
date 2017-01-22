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
import WebCam
import GripRunner
from config import debug, exposure, resolution

try:
	import NetworkTabling
except:
	if debug:
		print "no networktables"

if debug:
	from Printing import printResults

def main():
	WebCam.set(exposure=exposure, resolution=resolution)
	while True:
		runVision() #count frame nums if necessary
	runVision()


def runVision():

	image = WebCam.getImage()
	contours = GripRunner.run(image)
	targets = filterContours(contours) # To be edited if the last filter is changed in case of algorithmic changes. 
	center = findCenter(targets) #if 2, join and find center, if 1, return val, if 0 return input. if adjustCoords:	center[0] -= halfWidth
	if debug:
		printResults(image, contours, targets, center)
	try:
		NetworkTabling.publishToTables(center)
	except:
		pass

if __name__ == '__main__':
	main()
