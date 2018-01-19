import cv2
import numpy as np
from ContourFinding import filterContours, filterContoursFancy
from SpikeFinding import findSpike
import config, WebCam, GripRunner, autocalibrate, NetworkTabling, Printing

def main():
	lastAngle = 0
	WebCam.set(exposure=config.exposure, resolution=config.resolution, contrast=config.contrast, gain=config.gain)
	if config.autocalibrate:
		autocalibrate.calibrate()
	if config.debug:
		print "Exposure: ", WebCam.getExposure()
	config.resolution = WebCam.getResolution()
	config.degPerPxl = np.divide(config.nativeAngle, config.resolution)
	if not config.edited:
		GripRunner.editCode()
	if config.display:
		cv2.namedWindow("Contours Found")
	frameNum = 1
	while True:
		if NetworkTabling.checkForCalibrate():
			print "CALIBRATING the camera due to button press"
			autocalibrate.calibrate()
			NetworkTabling.putCalibrated()

		image = WebCam.getImage()
		contours = GripRunner.run(image)
		targets = filterContoursFancy(contours)
		isVisible, angleToGoal, distance = findSpike(targets)
		if lastAngle != 0 and not isVisible:
			angleToGoal = lastAngle
		else:
			lastAngle = angleToGoal
		if config.debug:
			Printing.printResults(contours=contours, distance=distance, angleToGoal=angleToGoal, isVisible=isVisible)
		if config.save:
			Printing.save(image)
		if config.display:
			Printing.drawImage(image, contours, targets)
			Printing.display(image)
		if config.save:
			Printing.save(image, withGrip=True)

		try:
			NetworkTabling.publishToTables(isVisible=isVisible, angleToGoal=angleToGoal, distance=distance, frameNum=frameNum)
		except Exception as error:
			if config.debug:
				print error
		frameNum += 1
	if display:
		cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
