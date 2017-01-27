

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
import GripRunner
from config import debug, display, sampleImage, edited
import NetworkTabling


if debug:
	import Printing

def main():
	if not edited:
		GripRunner.editCode()
	image = cv2.imread(sampleImage)
	contours = GripRunner.run(image)
	targets = filterContours(contours) # To be edited if the last filter is changed in case of algorithmic changes. 
	center = findCenter(targets) #if 2, join and find center, if 1, return val, if 0 return input. if adjustCoords:	center[0] -= halfWidth
	print center
	if debug:
		image = Printing.printResults(image, contours, targets, center)
		if display:
			Printing.display(image)
	try:
		NetworkTabling.publishToTables(center)
	except:
		print "The networktables are mean to us"

if __name__ == '__main__':
	main()
