import cv2

def printResults(contours, spikePostion, image):
	print "Started with {} contours".format(len(contours))
	print "spike x position is {}".format(spikePostion[0])
	print "spike y position is {}".format(spikePostion[1])

	# for i in range(len(contours)):
		# cv2.drawContours(image, contours[i], -1, (255,0,0), 3, 20)	
	cv2.drawContours(image, contours, -1, (255,0,0), 3, 20)
	cv2.circle(image, spikePostion, 10, (255, 255, 255), 20)
	img = cv2.resize(image ,None,fx=0.3, fy=0.3, interpolation = cv2.INTER_CUBIC)
	cv2.imshow("Contours Found", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
