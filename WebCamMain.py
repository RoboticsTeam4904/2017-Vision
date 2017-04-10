import cv2
import numpy as np
import config, GripRunner, NetworkTabling, SpikeFinding, ContourFinding, Printing, WebCam, autocalibrate

def main():
	WebCam.set(exposure=config.exposure, resolution=config.resolution, contrast=config.contrast, gain=config.gain)
	if config.autocalibrate:
		autocalibrate.calibrate()
	if config.debug:
		print "Exposure: ", WebCam.getExposure()
	if config.display:
		cv2.namedWindow("Contours Found")
	frameNum = 1
	lastAngle = 0
	while True:
		if NetworkTabling.checkForCalibrate():
			print "CALIBRATING the camera due to button press"
			autocalibrate.calibrate()
			NetworkTabling.putCalibrated()

		image = WebCam.getImage()
		contours = GripRunner.run(image)
		targets = ContourFinding.filterContours(contours)
		isVisible, angleToGoal, distance = SpikeFinding.findSpike(targets)
		if lastAngle != 0 and not isVisible:
			angleToGoal = lastAngle
		else:
			lastAngle = angleToGoal

		try:
			NetworkTabling.publishToTables(isVisible=isVisible, angleToGoal=angleToGoal, distance=distance, frameNum=frameNum)
		except Exception as error:
			if config.debug:
				print error

		if config.debug:
			Printing.printResults(contours=contours, distance=distance, angleToGoal=angleToGoal, isVisible=isVisible)
		if config.save and frameNum % config.saveFrequency:
			Printing.save(image)
			Printing.drawImage(image, contours, targets)
			Printing.save(image, withGrip=True)
		if config.display:
			Printing.drawImage(image, contours, targets) # redraws in case of save and display (that's ok)
			Printing.display(image)
		frameNum += 1

if __name__ == '__main__':
	main()
