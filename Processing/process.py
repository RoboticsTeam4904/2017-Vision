import editGrip # Creates grip_edited 
from grip_edited import GripPipeline
pipeline = GripPipeline()

import filtering

def process(image):
	pipeline.process(image)
	contours = pipeline.filter_contours_output
	filteredContours = filtering.filter(contours)
	return filteredContours
