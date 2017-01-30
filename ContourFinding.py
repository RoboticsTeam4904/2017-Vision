import cv2, copy
import numpy as np
import Printing
import config


minContours = 2

polyWeight = 10
ratioWeight = 50
toEdgesWeight = 1
areaWeight = 5
weights = np.array([polyWeight, ratioWeight, toEdgesWeight, areaWeight])

def filterContours(contours):
	numContours = len(contours)
	# if debug:
	# 	print "Number of contours: {}".format(numContours)
	if numContours > 1:
		# Find 2 largest contours.
		largest_contour, second_largest_contour, largest_area, second_largest_area = None, None, 0, 0
		for i in range(numContours):
			temp_area = cv2.contourArea(contours[i], False)
			if temp_area > second_largest_area:
				if temp_area > largest_area:
					largest_contour, second_largest_contour = contours[i], largest_contour
					largest_area, second_largest_area = temp_area, largest_area
				else:
					second_largest_contour = contours[i]
					second_largest_area = temp_area
		return largest_contour, second_largest_contour
	else:
		return contours

def filterContoursFancy(contours, image=None):
	numContours = len(contours)
	areas = np.array([cv2.contourArea(contour) for contour in contours])

	rotatedRects = [cv2.minAreaRect(contour) for contour in contours]
	rotatedBoxes = [cv2.boxPoints(rect) for rect in rotatedRects]
	boundingRects = [cv2.boundingRect(contour) for contour in contours]
	quads = [Quadrify(contour) for contour in contours]

	
	scores = np.array([polyScores, ratioScores, toEdgesScores, areaScores])
	contourScores = np.dot(weights, scores)
	sortedScoresIndices = contourScores.argsort()
	correctContours = np.array(contours)[sortedScoresIndices[:minContours]]

	if config.extra_debug:
		print "poly, ratio, toEdges, area"
		print "Weights", weights
		print "scores", contourScores
		# scores = np.multiply(scores, weights)
		for i in range(numContours):
			img = copy.deepcopy(image)
			print "CONTOUR " + str(i)
			print np.multiply(scores[:, i], weights) #newWeights
			print contourScores[i]
			Printing.drawImage(img, contours[:i] + contours[i+1:], contours[i], False)
			Printing.display(img, "contour " + str(i), defaultSize=True)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	return correctContours

def boundingInfo(rects):
	rects = np.array(rects)
	widths = rects[:,2]
	heights = rects[:,3]
	positions = rects[:,:2]
	return widths, heights, positions

def rotatedInfo(rects):
	widths, heights = np.array([]), np.array([])
	for rect in rects:
		widths.append(rect[1][0])
		heights.append(rect[1][1])
		# center = rect[0] + rotate(rect[1] by angles)
	return widths, heights

def distToPolygon(contour, polygon):
	tests = [cv2.pointPolygonTest(polygon, (point[0][0], point[0][1]), True) for point in contour]
	return np.average(np.absolute(tests))
	# (point[0][0], point[0][1]) replace with point?

def rotatation(rotatedRect):
	return np.abs(rotatedRect[2])

def sizeTest(area):
	# DONT DO MAYBE
	# Too large bad, too small bad
	pass

# The dimensions of the tape is 2 x 5 inches, so expect ed height is 1.5 times the width	
def ratios(widths, heights):
	ratios = np.divide(np.true_divide(heights, widths), 1.5)
	ratioScores = np.absolute(np.log(ratios))
	# Subtract the difference from what is expected from that contour's score
	# contourScores[i] -= abs(heights[i] - widths[i]*1.5)
	# Log instead of subtraction so it scales

# def multipleRatioTest(rectOne, rectTwo):
# 	Same width (same height, stuff)
# 	https://wpilib.screenstepslive.com/s/4485/m/24194/l/683625-processing-images-from-the-2017-frc-game maybe

# The more points are on the very edges of the shape, the more verticle the left and right sides are, meaning it is
# more likely to be a rectangle, which is what we want
def toEdges(contours): #DEPRACATED
	xCoords = [contour[:,0,0] for contour in contours]
	xDistances = np.subtract(xCoords, positions[:,0])
	otherXDistances = np.add(xDistances, widths)
	minXDistances = [np.minimum(xDistance, otherXDistance) for xDistance, otherXDistance in zip(xDistances,otherXDistances)]
	toEdgesScores = [np.average(minXDistance) for minXDistance in minXDistances]
	toEdgesScores = np.true_divide(toEdgesScores, widths)


def polygonAreaDiff(areas, polyAreas):
	ratios = np.divide(rotatedAreas, areas)
	return np.absolute(np.log(ratios))
	# cv2.contourArea(poly)


def Quadrify(contour):
	epsilon = 10
	for i in range(10):
		quad = cv2.approxPolyDP(contour, epsilon, True)
		length = len(quad)
		randomVar = np.random.random()
		epsilon = np.multiply(epsilon, np.true_divide(length+randomVar, 4+randomVar))
		# print epsilon, length
		if length == 4:
			return quad
	return False



# Parallelograms everywhere. Otherwise quads or minarearectangle
# Perimeter
# More ratios (check wpilib)
# What about spike? Test image, test scores. How to get around it
# Paired or triplet contours
# Run approxPoly once and record num sides?


# convexity defects
# floodfill



	# correct = contourScores[sortedScoresIndices[:minContours]]
	# incorrect = contourScores[sortedScoresIndices[minContours:]]
	# avgCorrect = np.average(correct)
	# avgIncorrect = np.average(incorrect)
	# avgdiffs = np.subtract(avgIncorrect, avgCorrect)
	# newWeights = np.multiply(weights, avgdiffs)
	


	# # Pairs all contours with each other, and checks that the bounding rectangle around
	# # both of them is the dimensions that it should be
	# print "scores", ratioScores
	# print toEdgesScores
	# print areaScores

	# correctContours = sortedContours[:minContours]




	# print "scores", contourScores
	# correct = contourScores[sortedScoresIndices[:minContours]]
	# incorrect = contourScores[sortedScoresIndices[minContours:]]
	# worstCorrect = np.amax(correct)
	# bestIncorrect = np.amin(incorrect)
	# worstdiff = np.divide(bestIncorrect, worstCorrect)
	# print "olddiff", worstdiff
	# avgCorrect = np.average(correct)
	# avgIncorrect = np.average(incorrect)
	# avgdiff = np.divide(avgIncorrect, avgCorrect)
	# print "oldavgdiff", avgdiff
	# correct = scores[:,sortedScoresIndices[:minContours]]
	# incorrect = scores[:,sortedScoresIndices[minContours:]]
	# worstCorrect = np.amax(correct, axis=1)
	# bestIncorrect = np.amin(incorrect, axis=1)
	# worstdiffs = np.subtract(bestIncorrect, worstCorrect)
	# # worstdiffs = np.multiply(worstdiffs, weights)
	# print "worstdiffs", worstdiffs
	# avgCorrect = np.average(correct, axis=1)
	# avgIncorrect = np.average(incorrect, axis=1)
	# avgdiffs = np.subtract(avgIncorrect, avgCorrect)
	# # avgdiffs = np.multiply(avgdiffs, weights)
	# # newWeights = np.multiply(np.multiply(avgdiffs, worstdiffs),weights)
	# newWeights = np.multiply(avgdiffs,weights)
	# print newWeights
	# contourScores = np.dot(np.transpose(scores), newWeights)
	# print "avgdiffs", avgdiffs
	# print "scores", contourScores
	# correct = contourScores[sortedScoresIndices[:minContours]]
	# incorrect = contourScores[sortedScoresIndices[minContours:]]
	# worstCorrect = np.amax(correct)
	# bestIncorrect = np.amin(incorrect)
	# worstdiff = np.divide(bestIncorrect, worstCorrect)
	# print "newdiff", worstdiff
	# avgCorrect = np.average(correct)
	# avgIncorrect = np.average(incorrect)
	# avgdiff = np.divide(avgIncorrect, avgCorrect)
	# print "newavgdiff", avgdiff