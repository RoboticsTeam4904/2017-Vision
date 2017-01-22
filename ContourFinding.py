import cv2

def filterContours(contours, debug):
	numContours = len(contours)
	if debug:
		print "Number of contours: {}".format(numContours)
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
