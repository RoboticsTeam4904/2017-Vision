import cv2
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

def filterContoursFancy(contours, image):



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

	polyWeight = 0.3
	ratioWeight = 20
	toEdgesWeight = 10
	areaWeight = 5

	
	# Calculate a score for each contour that is the probability that it is correct
	# contourScores = np.zeroes(len(contours))
	# polygons = [cv2.approxPolyDP(contour, margin, True) for contour in contours]
	# polygons = [Quadrify(contour) for contour in contours]
	# polyScores = [np.average([cv2.pointPolygonTest(poly, (point[0][0], point[0][1]), True) for point in contour]) for poly,contour in zip(polygons, contours)]
	polyScores = np.zeros(numContours)

	# The dimensions of the tape is 2 x 5 inches, so expect ed height is 1.5 times the width
	ratios = np.divide(np.true_divide(heights, widths), 1.5)
	ratioScores = np.absolute(np.log(ratios))
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
	# boungingRectangles = [cv2.minAreaRect(contour)[2:] for contour in contours] # TODO: Enhancement
	boundingRectangles = np.array([cv2.boundingRect(contour) for contour in contours])
	boundingAreas = np.multiply(boundingRectangles[:,2], boundingRectangles[:,3])
	areas = [cv2.contourArea(contour) for contour in contours]
	areaScores = np.absolute(np.log(np.divide(boundingAreas, areas)))

	weights = np.array([polyWeight, ratioWeight, toEdgesWeight, areaWeight])
	scores = np.array([polyScores, ratioScores, toEdgesScores, areaScores])
	contourScores = np.dot(weights, scores)

	# Return which contours are above the threshold, then lower the threshold if no contours
	# would be returned
	# sortedScores = np.sort(contourScores)
	# correctContours = [contours[contourScores.index(contour)] for contour in sortedScores[-minContours:]]
	# correctContours = [contour for score, contour in sorted(zip(contourScores, contours))]
	sortedScoresIndices = contourScores.argsort()
	sortedContours = np.array(contours)[sortedScoresIndices]
	# # Pairs all contours with each other, and checks that the bounding rectangle around
	# # both of them is the dimensions that it should be
	# print "scores", ratioScores
	# print toEdgesScores
	# print areaScores

	correctContours = sortedContours[:minContours]

	if config.extra_debug:
		print "poly, ratio, toEdges, area"
		print "Weights", weights
		for i in range(numContours):
			img = image
			print "CONTOUR " + str(i)
			print scores[:, i]
			print heights[i], widths[i]
			print ratios[i]
			Printing.drawContours(img, contours[i])
			img = Printing.resize(img)
			Printing.display(img, "contour " + str(i))

	print contourScores
	print sortedScoresIndices

	return correctContours

def Quadrify(contour):
	epsilon = 10
	quad = None
	length = 0
	while length != 4:
		quad = cv2.approxPolyDP(contour, epsilon, True)
		length = len(quad)
		epsilon = np.multiply(epsilon, np.true_divide(length, 4))
	return quad


