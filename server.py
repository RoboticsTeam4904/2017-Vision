from __future__ import division #Might take time to import
import SocketServer, subprocess, time, cv2, math
import numpy as np

pi = False
gui = True

if pi:
	from picamera.array import PiRGBArray
	from picamera import PiCamera


if pi:
	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	camera.resolution = (640, 480)
	camera.framerate = 15
	rawCapture = PiRGBArray(camera, size=camera.resolution)

# constants
cameraResolution = (640, 480)
nativeResolution = (2592, 1944)
nativeAngle = (math.radians(53.5), math.radians(41.41))
mountAngle = (0, math.radians(45))
shift = (13.25, 2.5)
goalHeight = 8 * 12
cameraHeight = 296 / 25.4 #to inches

def getImage():
	image = None

	if pi:
		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			image = frame.array

			# show the frame
			if debug:
				cv2.imshow("Frame", image)

			# clear the stream in preparation for the next frame
			rawCapture.truncate(0)
	else:
		image = cv2.imread("latest.jpg")

	return image

def angle_and_dist_BAD((x, y, w, h)):
	# [0] = X, [1] = Y, goal[i] = ith corner of highgoal
	# Uses camera.resolution
	degPerPxl = (nativeAngle[0] / cameraResolution[0], nativeAngle[1] / cameraResolution[1])
	goalPixel = (x + w/2, y + h/2)
	goalAngle = (mountAngle[0] + degPerPxl[0] * (goalPixel[0] - cameraResolution[0] / 2), mountAngle[1] + degPerPxl[1] * (goalPixel[1] - cameraResolution[1] / 2))
	cameraDistance = (goalHeight - cameraHeight) / math.tan(goalAngle[1])
	shiftTotal = math.sqrt(shift[0] * shift[0] + shift[1] * shift[1])
	cameraAngle = math.pi - goalAngle[0] - math.atan(shift[0] / shift[1])
	distance = math.sqrt(cameraDistance * cameraDistance + shiftTotal * shiftTotal - 2 * cameraDistance * shiftTotal * math.cos(cameraAngle))
	offAngle = math.asin(math.sin(cameraAngle) * cameraDistance / distance)
	offAngle += math.atan(shift[1] / shift[0]) - math.pi / 2
	return (offAngle, distance)

def angle_and_dist((x, y, w, h)):
	# [0] = X, [1] = Y, goal[i] = ith corner of highgoal
	# Uses camera.resolution
	degPerPxl = [nativeAngle[i] / cameraResolution[i] for i in range(2)]
	centerOfGoalPixelCoords = (x + w/2, y + h/2)
	goalAngle = [mountAngle[i] + degPerPxl[i] * (centerOfGoalPixelCoords[i] - cameraResolution[i] / 2) for i in range(2)]
	goalAngleLeftToRight=goalAngle[0]
	goalAngleUpAndDown=goalAngle[1]
	cameraToGoalDistance = (goalHeight - cameraHeight) / math.tan(goalAngleUpAndDown)


	cameraToGoalX=math.sin(goalAngleLeftToRight)*cameraToGoalDistance
	cameraToGoalY=math.cos(goalAngleLeftToRight)*cameraToGoalDistance
	centerOfRobotToGoalX=cameraToGoalX-shift[0]
	centerOfRobotToGoalY=cameraToGoalY+shift[1]
	centerOfRobotToGoalDist=math.sqrt(centerOfRobotToGoalX*centerOfRobotToGoalX+centerOfRobotToGoalY*centerOfRobotToGoalY)
	return (math.atan(centerOfRobotToGoalX/centerOfRobotToGoalY),centerOfRobotToGoalDist)

def processImage(src):
	offAngle = 0.0
	distance = 0.0

	thresholdValue = 200
	max_thresh = 255
	blob_size = 3

	if gui:
		cv2.imshow("original", src)

	grayscale = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)	#TODO: change to stripping just reds or something compute-easy convert image to black and white
	blurred = cv2.blur(grayscale, (3, 3))	# blur image
	ret, thresholded = cv2.threshold(blurred, thresholdValue, max_thresh, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	if gui:
		cv2.drawContours(grayscale, contours, -1, (0,255,0), 3)
		cv2.imshow("grayscaleafter", grayscale)
		cv2.imshow("thresholded", thresholded)

	hull = [cv2.convexHull(contour[0], False) for contour in contours]
	convex = np.zeros(thresholded.shape, dtype=np.uint8)
	cv2.drawContours(convex, hull, -1, (255,255,255), cv2.cv.CV_FILLED, 8)
	subtracted = cv2.bitwise_and(convex, cv2.bitwise_not(thresholded))

	if gui:
		cv2.imshow("convex", convex)
		cv2.imshow("subtracted", subtracted)

	# blob callback
	blobbed = np.zeros(subtracted.shape, dtype=np.uint8)
	element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * blob_size + 1, 2 * blob_size + 1), (blob_size, blob_size))


	cv2.erode(subtracted, blobbed, element)
	cv2.dilate(blobbed, blobbed, element)

	if gui:
		cv2.imshow("blobbed", blobbed)

	contours, hierarchy = cv2.findContours(blobbed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# print contours

	# Find largest contour. Is slightly inefficient in the case of 1 contour
	if len(contours) > 0:
		largest_contour = contours[0]
		largest_area = cv2.contourArea(contours[0], False)
		for i in range(1, len(contours)):
			tempArea = cv2.contourArea(contours[i], False)
			if (temp_area > largest_area):
				largest_contour = contours[i]
				largest_area = temp_area
		goal = cv2.approxPolyDP(largest_contour, 3, True)
		data = angle_and_dist(goal)
		print "1::" + str(math.degrees(data[0])) + "::" + str(data[1])
		if gui:
			cv2.line(src, goal.side[0], goal.side[1], (255, 0, 0), 5)
			cv2.line(src, goal.side[1], goal.side[2], (255, 0, 0), 5)
			cv2.line(src, goal.side[2], goal.side[3], (255, 0, 0), 5)
			cv2.line(src, goal.side[3], goal.side[0], (255, 0, 0), 5)
			c2.imshow("window", src)
	else:
		print "0::0::0"

	if gui:
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	return 0


class MyTCPHandler(SocketServer.BaseRequestHandler):
    # Responds to requests for the view of the goal.

    def handle(self):
        # self.request is the TCP socket connected to the client
        #process = subprocess.Popen(["./highgoal.bin", "latest"], stdout=subprocess.PIPE)

        response = process.stdout.read()
        # just send back the same data, but upper-cased
        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    processImage(getImage())
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server this will keep running until you
    # interrupt the program with Ctrl-C
    #server.serve_forever()
