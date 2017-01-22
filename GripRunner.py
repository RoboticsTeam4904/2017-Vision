from grip import GripPipeline  # TODO change the default module and class, if needed
pipeline = GripPipeline()

def run(image):
	pipeline.process(image)
	return pipeline.filter_contours_output

def calibrate(hsv=False, area=False):
	if hsv:
		pipeline.__hsv_threshold_hue = hsv[0]
		pipeline.__hsv_threshold_saturation = hsv[1]
		pipeline.__hsv_threshold_value = hsv[2]
	if area:
		pipeline.__filter_contours_min_area = area
