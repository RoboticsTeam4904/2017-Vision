import cv2
import numpy as np
import config, GripRunner, NetworkTabling, SpikeFinding, ContourFinding, Printing, PiCamera

def main():
	PiCamera.set(exposure=config.exposure, resolution=config.resolution)
	config.resolution = PiCamera.getResolution()
	config.degPerPxl = np.divide(config.nativeAngle, config.resolution)
	if not config.edited:
		GripRunner.editCode()
	frameNum = 1
	while True:
		image = PiCamera.getImage()
		contours = GripRunner.run(image)
		targets = ContourFinding.filterContours(contours, image=image)
		isVisible, angleToGoal, distance = SpikeFinding.findSpike(targets)
		if config.debug:
			Printing.printResults(contours=contours, distance=distance, angleToGoal=angleToGoal, isVisible=isVisible)
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
