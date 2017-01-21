"""
Simple skeleton program for running an OpenCV pipeline generated by GRIP and using NetworkTables to send data.
Users need to:
1. Import the generated GRIP pipeline, which should be generated in the same directory as this file.
2. Set the network table server IP. This is usually the robots address (roborio-TEAM-frc.local) or localhost
3. Handle putting the generated code into NetworkTables
"""

import cv2
import numpy as np
from networktables import NetworkTables

pi = False
webcam = False

debug = False
continuous = True
edited = False
adjustCoords = False
withOpenCV3 = True

resolution = (640, 360)
if adjustCoords:
	halfWidth = resolution[0]/2

if not edited:
	import EditGeneratedGrip
	EditGeneratedGrip.editCode('grip.py', withOpenCV3=withOpenCV3)
from grip import GripVisionPipeline  # TODO change the default module and class, if needed

def main():
	if debug:
		global image
	pipeline = GripVisionPipeline()

	if pi:
		if continuous:
			from camera import camera
			from picamera.array import PiRGBArray
			camera.resolution = resolution
			rawCapture = PiRGBArray(camera, size=camera.resolution)
			if debug:
				print "Getting image..."
			for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
				rawCapture.truncate(0)
				image = frame.array
				processing(pipeline, image)
				if debug:
					print "Getting image..."
		else:
			import camera
			camera.camera.resolution = resolution
			if debug:
				print "Getting image..."
			image = camera.getImage()
			processing(pipeline, image)  # TODO add extra parameters if the pipeline takes more than just a single image

	elif webcam:
		camera = cv2.VideoCapture(0)
		camera.set(3, resolution[0])
		camera.set(4, resolution[1])
		# camera.set(15, 0.1) # exposure
		if continuous:
			while True:
				if debug:
					print "Getting image..."
				retval, image = camera.read()
				if retval:
					processing(pipeline, image)
		else:
			if debug:
				print "Getting image..."
			retval, image = camera.read()
			if retval:
				processing(pipeline, image)

	else: #sample image
		image = cv2.imread("TestImages/GearTest.png")
		processing(pipeline, image)


def findCenter(contours):
	numContours = len(contours)
	if debug:
		print "Number of contours: {}".format(numContours)
	if numContours > 1:
		# Find 2 largest contours.
		largest_contour = contours[0]
		second_largest_contour = contours[1]
		largest_area = cv2.contourArea(contours[0], False)
		second_largest_area = cv2.contourArea(contours[1], False)
		if second_largest_area > largest_area:
			largest_contour, second_largest_contour = largest_contour, second_largest_contour
			largest_area, second_largest_area = second_largest_area, largest_area
		for i in range(2, numContours):
			temp_area = cv2.contourArea(contours[i], False)
			if (temp_area > second_largest_area):
				second_largest_contour = contours[i]
				second_largest_area = temp_area
				if second_largest_area > largest_area:
					largest_contour, second_largest_contour = largest_contour, second_largest_contour
					largest_area, second_largest_area = second_largest_area, largest_area
		total_contour = np.concatenate((largest_contour, second_largest_contour))
		x, y, w, h = cv2.boundingRect(total_contour) # Works best when camera is horizontal relative to target
		center = (x+w/2, y+h/2)
		if debug:
			print "Found Center:", center
			cv2.drawContours(image, contours, -1, (70,70,0), 3)
			cv2.drawContours(image, [largest_contour], -1, (0,255,0), 3)
			cv2.drawContours(image, [second_largest_contour], -1, (0,0,255), 3)
			cv2.drawContours(image, [total_contour], -1, (255,0,0), 3)
			cv2.circle(image, center, 4, (255, 255, 255))
			cv2.imshow("Contours Found", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		return center
	elif numContours == 1:
		x, y, w, h = cv2.boundingRect(contours[0])
		center = (x+w/2, y+h/2)
		if debug:
			print "Found Center:", center
			print "1 contour found (no bueno)"
			cv2.drawContours(image, contours, -1, (70,70,0), 3)
			cv2.circle(image, center, 4, (255, 255, 255))
			cv2.imshow("Contours Found", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		return center
	else:
		if debug:
			print "RIP. no contours."
		return (0,0)

def processing(pipeline, image):
	"""
	Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
	:param pipeline: the pipeline that just processed an image
	:return: None

	"""
	if debug:
		print "Got image. Analyzing image (pipeline process)..."
	pipeline.process(image)  # TODO add extra parameters if the pipeline takes more than just a single image
	if debug:
		print "Image processed. Analyzing contours..."
	targets = pipeline.filter_contours_output # To be edited if the last filter is changed in case of algorithmic changes.
	center = findCenter(targets)
	#######################
	# NetworkTables stuff #
	#######################
	if debug:
		print "Analyzed. Publishing to network tables..."

	if adjustCoords:
		center[0] -= halfWidth
	
def publishToTables(center, calibrate=False):
		
	
	NetworkTables.setTeam(4904)
	ip = "10.49.4.2"
	NetworkTables.initialize(server=ip)
	network = NetworkTables.getTable("SmartDashboard")

	# if calibrate:
		#pipeline.calibrate(hsv_threshold_hue=network.getNumber('hsv_threshold_hue'), hsv_threshold_saturation=network.getNumber('hsv_threshold_value'), hsv_threshold_value=network.getNumber('hsv_threshold_value'))

	network.putNumber('centerX', center[0])
	network.putNumber('centerY', center[1])

	if debug:
		print "Published to network tables."

if __name__ == '__main__':
	main()
