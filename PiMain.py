import cv2
import numpy as np
from ContourFinding import filterContoursFancy
from SpikeFinding import findSpike
import PiCamera
import GripRunner
import config
import NetworkTabling

if debug:
	import Printing

def main():
	PiCamera.set(exposure=config.exposure, resolution=config.resolution)
	config.resolution = PiCamera.getResolution()
	if not config.edited:
		GripRunner.editCode()
	frameNum = 1
	while True:
		image = PiCamera.getImage()
		contours = GripRunner.run(image)
		targets = filterContoursFancy(contours)
		isVisible, angleToGoal, distance = findSpike(targets)
		if config.debug:
			Printing.printResults(contours, center)
		if config.save:
			Printing.drawImage(image, contours, targets, center)
			Printing.save(image)
		try:
			NetworkTabling.publishToTables(isVisible=isVisible, angleToGoal=angleToGoal, distance=distance, frameNum=frameNum)
		except Exception as error:
			if config.debug:
				print error
		frameNum += 1

if __name__ == '__main__':
	main()
