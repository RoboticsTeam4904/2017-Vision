import numpy as np
import cv2
import sys

imageNum = 0
colors = [(255,255,255), (255,255,0), (50,50,255)]
defaultSize = (640,360)
defaultShrinkX, defaultShrinkY = 0.3, 0.3
defaultThickness = 5
imageName = "img"
gripImageName = "contours"
rand = "match" + str(np.random.randint(1000)) + "-"

def printResults(contours=False, distance=False, angleToGoal=False, isVisible=True, center=False):
	if not isVisible:
		print "CANNOT SEE GOAL"
	if contours:
		print "{} contours".format(len(contours))
	if distance:
		print "{} feet away".format(distance)
	if angleToGoal:
		print "{} degrees off".format(angleToGoal)
	if center:
		print "spike x position is {}".format(center[0])
		print "spike y position is {}".format(center[1])


def drawImage(image, contours, targets, center=False):
	drawContours(image, contours)
	drawContours(image, targets, color=2)
	if center:
		drawCenter(image, center)

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

def save(image, name=None, withGrip=False, withRand=False):
	if name != None:
		cv2.imwrite("TestImages/" + name + ".jpg", image)
		return
	if withGrip:
		name = gripImageName
	else:
		name = imageName
	if withRand:
		name = rand + name
	global imageNum
	name += str(imageNum)
	cv2.imwrite("TestImages/" + name + ".jpg", image)
	imageNum += 1

def display(image, name="Contours Found", doResize=True):
	if doResize:
		image = resize(image)
	cv2.imshow(name, image)
	key = cv2.waitKey(20)
	if key == 27:
		sys.exit()
