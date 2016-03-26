from __future__ import division #Might take time to import
import SocketServer, subprocess, time, cv2, math
import numpy as np

pi = False

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
inToMm = 25.4
nativeResolution = (2592, 1944)
nativeAngle = (math.radians(53.5), math.radians(41.41))
mountAngle = (0, math.radians(45))
shift = (13.25 * inToMm, 2.5 * inToMm)
goalHeight = 8 * 12 * inToMm
cameraHeight = 296

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

def angle_and_dist(goal):
	# [0] = X, [1] = Y, goal[i] = ith corner of highgoal
	# Uses camera.resolution
	degPerPxl = (nativeAngle[0] / camera.resolution[0], nativeAngle[1] / camera.resolution[1])
	goalPixel = ((goal[0].x + goal[1].x + goal[2].x + goal[3].x) / 4, camera.resolution[1] - (goal[0].y + goal[1].y + goal[2].y + goal[3].y) / 4)
	goalAngle = (mountAngle[0] + degPerPxl[0] * (goalPixel[0] - camera.resolution[0] / 2), mountAngle[1] + degPerPxl[1] * (goalPixel[1] - camera.resolution[1] / 2))
	cameraDistance = (goalHeight - cameraHeight) / math.tan(goalAngle[1])
	shift = math.sqrt(shift[0] * shift[0] + shift[1] * shift[1])
	cameraAngle = math.pi - goalAngle[0] - math.atan(shift[0] / shift[1])
	distance = math.sqrt(cameraDistance * cameraDistance + shift * shift - 2 * cameraDistance * shift * math.cos(cameraAngle))
	offAngle = math.asin(math.sin(cameraAngle) * cameraDistance / distance)
	offAngle += math.atan(shift[1] / shift[0]) - math.pi / 2
	distance /= inToMm
	return (offAngle, distance)

def processImage(src):
	offAngle = 0.0
	distance = 0.0

	thresholdValue = 230
	max_thresh = 255
	blob_size = 3

	goalFound = 0


	grayscale = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)	#TODO: change to stripping just reds or something compute-easy convert image to black and white
	#blurred = cv2.blur(grayscale, (3, 3))	# blur image
	ret, thresholded = cv2.threshold(grayscale, thresholdValue, max_thresh, cv2.THRESH_BINARY)
	#cv2.imshow("grayscalebefore", grayscale)

	#cv2.imshow("original", src)
	#cv2.imshow("threshold", thresholded)

	contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	cv2.drawContours(grayscale, contours, -1, (0,255,0), 3)

	if gui:
		cv2.imshow("grayscaleafter", grayscale)
		cv2.imshow("thresholded", thresholded)

	hull, tempConvex = [], []
	for i in range(len(contours)):
		cv2.convexHull(Mat(contours[i]), tempConvex, false)
		hull += [tempConvex]

	convex = np.zeros(len(thresholded))
	for i in range(len(contours)):
		cv2.drawContours(convex, hull, i, Scalar(255,255,255), CV_FILLED, 8, vector<Vec4i>(), 0, Point() )

	subtracted = cv2.bitwiseAnd(convex, cv2.bitwiseNot(thresholded))

	if gui:
		cv2.imshow("convex", convex)
		cv2.imshow("subtracted", subtracted)

	# blob callback
	poly, largest_contour, hierarchy, blobbed = [], [], [], []
	element = getStructuringElement(MORPH_ELLIPSE, Size(2 * blob_size + 1, 2 * blob_size + 1), Point(blob_size, blob_size))

	cv2.erode(subtracted, blobbed, element)
	cv2.dilate(blobbed, blobbed, element)

	if gui:
		cv2.imshow("blobbed", blobbed)

	cv2.findContours(blobbed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0))

	# Find largest contour. Is slightly inefficient in the case of 1 contour
	if len(contours) > 0:
		goalFound = true
		largest_area = 0.0
		for i in range(len(contours)):
			# Find the area of contour
			tempArea = cv2.contourArea(contours[i], false)
			if (temp_area > largest_area):
				largest_contour = contours[i]
				largest_area = temp_area

	if goalFound:
		goal = cv2.approxPolyDP(Mat(largest_contour), 3, true)
		data = angle_and_dist(goal)
		print "1::" + str(math.degrees(data[0])) + "::" + str(data[1])
	else:
		print "0::0::0"

	if gui:
		line(result, goal.side[0], goal.side[1], Scalar(255, 0, 0), 5)
		line(result, goal.side[1], goal.side[2], Scalar(255, 0, 0), 5)
		line(result, goal.side[2], goal.side[3], Scalar(255, 0, 0), 5)
		line(result, goal.side[3], goal.side[0], Scalar(255, 0, 0), 5)
		c2.imshow("window", result)

		cv2.waitKey(0)
		cv2.destroyAllWindows()
		
	return 0



	"""
	if gui:
		imshow("threshold", threshold_output)


	findContours(threshold_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0))
	for i in range(len(contours)):
		convexHull(Mat(contours[i]), hull[i], false)

	convex = Mat::zeros( threshold_output.size(), CV_8UC1 )
	for (int i = 0 i<contours.size() ++i)
		drawContours(convex, hull, i, Scalar(255,255,255), CV_FILLED, 8, vector<Vec4i>(), 0, Point() )


	subtracted = np.zeros((height,width,1), np.uint8)

	if (convex.isContinuous() && threshold_output.isContinuous())
		uchar *p1, *p2, *p3
		p1 = convex.ptr<uchar>(0)
		p2 = threshold_output.ptr<uchar>(0)
		p3 = subtracted.ptr<uchar>(0)
		for (int i = 0 i < convex.rows * convex.cols ++i)
			if (*p2 != 0)
				*p3 = 0
			 else if (*p1 != 0)
				*p3 = 255

			p1++
			p2++
			p3++



	# subtract(convex, threshold_output, subtracted)

	if (gui && detailedGUI)
		imshow("convex", convex)
		imshow("subtracted", subtracted)


	# blob callback

	vector<Point> poly, largest_contour
	vector<Vec4i> hierarchy
	Mat blobbed
	Mat element = getStructuringElement(MORPH_ELLIPSE, Size(2 * blob_size + 1, 2 * blob_size + 1), Point(blob_size, blob_size))

	erode(subtracted, blobbed, element)
	dilate(blobbed, blobbed, element)
	if (gui && detailedGUI) imshow("blobbed", blobbed)
	findContours(blobbed, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0))
	Mat result = src.clone()
	# Mat::zeros(blobbed.size(), CV_8UC3)

	if (contours.size()!=0)
		existingGoal = true
		double largest_area = 0.0
		for (int i = 0 i < contours.size() i++)
			# Find the area of contour
			double a = contourArea(contours[i], false)
			if (a > largest_area)
				largest_contour = contours[i]
				largest_area = a



	approxPolyDP(Mat(largest_contour), poly, 3, true)
	goal.side_one = poly[0]
	goal.side_two = poly[1]
	goal.side_three = poly[2]
	goal.side_four = poly[3]

	if gui:
		line(result, goal.side_one, goal.side_two, Scalar(255, 0, 0), 5)
		line(result, goal.side_two, goal.side_three, Scalar(255, 0, 0), 5)
		line(result, goal.side_three, goal.side_four, Scalar(255, 0, 0), 5)
		line(result, goal.side_four, goal.side_one, Scalar(255, 0, 0), 5)
		imshow("window", result)"""


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
