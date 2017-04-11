import cv2
import numpy as np
import config, GripRunner, NetworkTabling, SpikeFinding, ContourFinding, Printing, PiCamera, Autocalibrate

def main():
	PiCamera.set(exposure=config.exposure, resolution=config.resolution)
	if config.debug:
		print "Shutter Speed: ", PiCamera.getShutterSpeed()
	if config.display:
		cv2.namedWindow("Contours Found")
	frameNum = 1
	lastAngle = 0
	while True:
		if NetworkTabling.checkForCalibrate():
			print "CALIBRATING the camera due to button press"
			Autocalibrate.calibrate()
			NetworkTabling.putCalibrated()

		image = PiCamera.getImage()
		contours = GripRunner.run(image)
		targets = ContourFinding.filterContours(contours)
		isVisible, angleToGoal, distance = SpikeFinding.findSpike(targets)
		if lastAngle != 0 and not isVisible:
			angleToGoal = lastAngle
		else:
			lastAngle = angleToGoal
		if config.debug:
			Printing.printResults(contours=contours, distance=distance, angleToGoal=angleToGoal, isVisible=isVisible)
		if config.save and frameNum % config.saveFrequency == 0:
			Printing.save(image)
		if config.display:
			Printing.drawImage(image, contours, targets)
			Printing.display(image)
		if config.save and frameNum % config.saveFrequency == 0:
			Printing.save(image, withGrip=True)

		try:
			NetworkTabling.publishToTables(isVisible=isVisible, angleToGoal=angleToGoal, distance=distance, frameNum=frameNum)
		except Exception as error:
			if config.debug:
				print error
		frameNum += 1

if __name__ == '__main__':
	main()
