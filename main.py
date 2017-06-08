import cv2
import numpy as np
# import Processing/process
import config, Coms.NetworkTabling, GripRunner, NetworkTabling, SpikeFinding, ContourFinding, Printing, Autocalibrate

if config.pi:
	import Camera.PiCam as camera
else:
	import Camera.WebCam as camera

def main():
	frameNum = 1
	lastAngle = 0
	while True: #use itertools to iterate frameNum
		NetworkTabling.calibrateIfButton()
		image = camera.getImage()
		contours = process.process(image)
		measurements = Measuring.measure(contours)
		if measurements.isVisible:
			lastAngle = angleToGoal
		else:
			angleToGoal = lastAngle

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
