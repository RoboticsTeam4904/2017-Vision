import cv2, copy
import numpy as np
import Printing
import config

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

	if numContours <= 1:
		return contours

	widths = []
	heights = []
	positions = []

	for contour in contours:
		x,y,w,h = cv2.boundingRect(contour)
		heights.append(h)
		widths.append(w)
		positions.append((x, y))

	widths, heights, positions = np.array(widths), np.array(heights), np.array(positions)

	scoreThreshold = -1
	minContours = 2

	polyWeight = 10
	ratioWeight = 50
	toEdgesWeight = 1
	areaWeight = 5

	
	# Calculate a score for each contour that is the probability that it is correct
	# contourScores = np.zeroes(len(contours))
	quads = [Quadrify(contour) for contour in contours]
	rotatedRectangles = np.array([cv2.boxPoints(cv2.minAreaRect(contour)) for contour in contours])
	polyScores = [np.average(np.divide(np.absolute([cv2.pointPolygonTest(poly, (point[0][0], point[0][1]), True) for point in contour]),width)) if type(poly) == np.ndarray else 1 for poly,contour,width in zip(rotatedRectangles, contours, widths)]

	# The dimensions of the tape is 2 x 5 inches, so expect ed height is 1.5 times the width
	ratios = np.divide(np.true_divide(heights, widths), 1.5)
	ratioScores = np.absolute(np.log(ratios))
	ratioScores = np.divide(ratioScores, widths)
	# Subtract the difference from what is expected from that contour's score
	# contourScores[i] -= abs(heights[i] - widths[i]*1.5)
	# Log instead of subtraction so it scales


	# The more points are on the very edges of the shape, the more verticle the left and right sides are, meaning it is
	# more likely to be a rectangle, which is what we want
	xCoords = [contour[:,0,0] for contour in contours]
	xDistances = np.subtract(xCoords, positions[:,0])
	otherXDistances = np.add(xDistances, widths)
	minXDistances = [np.minimum(xDistance, otherXDistance) for xDistance, otherXDistance in zip(xDistances,otherXDistances)]
	toEdgesScores = [np.average(minXDistance) for minXDistance in minXDistances]
	toEdgesScores = np.true_divide(toEdgesScores, widths)
	# Make better using cv2.minAreaRect(contour) at some point. This is a rotated rectangle

	# Create a bounding rectangle around each contour, and then see what percentage
	# of the rectangle is filled by the contour. The more the better.
	# print "W*YIUWDH", rotatedRectangles
	# boundingRectangles = np.array([cv2.boundingRect(contour) for contour in contours])
	# boundingAreas = np.multiply(boundingRectangles[:,2], boundingRectangles[:,3])
	rotatedAreas = [cv2.contourArea(rotatedRectangle) for rotatedRectangle in rotatedRectangles]
	areas = [cv2.contourArea(contour) for contour in contours]
	areaScores = np.absolute(np.log(np.divide(rotatedAreas, areas)))
	# quadAreas = [cv2.contourArea(quad) if type(quad) == np.ndarray else 100 for quad in quads]
	# areaScores = np.absolute(np.log(np.divide(quadAreas, areas)))

	weights = np.array([polyWeight, ratioWeight, toEdgesWeight, areaWeight])
	scores = np.array([polyScores, ratioScores, toEdgesScores, areaScores])
	contourScores = np.dot(weights, scores)
	sortedScoresIndices = contourScores.argsort()

	correct = contourScores[sortedScoresIndices[:minContours]]
	incorrect = contourScores[sortedScoresIndices[minContours:]]
	avgCorrect = np.average(correct)
	avgIncorrect = np.average(incorrect)
	avgdiffs = np.subtract(avgIncorrect, avgCorrect)
	newWeights = np.multiply(weights, avgdiffs)

	# Return which contours are above the threshold, then lower the threshold if no contours
	# would be returned
	# sortedScores = np.sort(contourScores)
	# correctContours = [contours[contourScores.index(contour)] for contour in sortedScores[-minContours:]]
	# correctContours = [contour for score, contour in sorted(zip(contourScores, contours))]
	contourScores = np.dot(newWeights, scores)
	sortedScoresIndices = contourScores.argsort()
	correctContours = np.array(contours)[sortedScoresIndices[:minContours]]


	# # Pairs all contours with each other, and checks that the bounding rectangle around
	# # both of them is the dimensions that it should be
	# print "scores", ratioScores
	# print toEdgesScores
	# print areaScores

	# correctContours = sortedContours[:minContours]

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
	print "hi"
	return False



# Parallelograms everywhere. Otherwise quads or minarearectangle
# Perimeter
# More ratios (check wpilib)
# What about spike? Test image, test scores. How to get around it
# Paired or triplet contours
# Run approxPoly once and record num sides?


# convexity defects
# floodfill





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