import numpy as np
import cv2

imageNum = 0
colors = [(255,255,255), (255,255,0), (50,50,255)]
defaultSize = (640,360)
defaultShrinkX, defaultShrinkY = 0.3, 0.3
defaultThickness = 5

def printResults(image, contours, targets, center):
	print "Started with {} contours".format(len(contours))
	if center:
		print "spike x position is {}".format(center[0])
		print "spike y position is {}".format(center[1])
	else:
		print "Could not find center!"
	drawContours(image, contours)
	drawContours(image, targets, color=2)
	if center:
		drawCenter(image, center)
	image = resize(image)
	#display(image)

def resize(image, size=defaultSize):
	return cv2.resize(image, size)

def shrink(image, x=defaultShrinkX, y=defaultShrinkY):
	return cv2.resize(image, 0, fx=x, fy=y)

def drawContours(image, contours, color=1, thickness=5):
	if type(color) == int:
		color = colors[color]
	if type(contours) == np.ndarray:
		if len(contours.shape) == 3:
			contours = [contours]
	cv2.drawContours(image, contours, -1, color, thickness)

def drawCenter(image, center, size=defaultThickness, color=0):
	if type(color) == int:
		color = colors[color]
	cv2.circle(image, center, size, color, size)

def save(image):
	global imageNum
	name="image{}.jpg".format(imageNum)
	cv2.imwrite("TestImages/" + name, image)
	imageNum += 1
def display(image, name="Contours Found"):
	cv2.imshow(name, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

