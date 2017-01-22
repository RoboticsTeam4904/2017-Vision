def initializeGrip(doc, edited, withOpenCV3):
	if not edited:
		import EditGeneratedGrip
		EditGeneratedGrip.editCode(doc, withOpenCV3=withOpenCV3)
	from grip import GripVisionPipeline  # TODO change the default module and class, if needed
	global pipeline
	pipeline = GripVisionPipeline()

def run(image):
	pipeline.process(image)
	return pipeline.filter_contours_output

def calibrate(hsv=False, area=False):
	if hsv:
		self.__hsv_threshold_hue = hsv[0]
		self.__hsv_threshold_saturation = hsv[1]
		self.__hsv_threshold_value = hsv[2]
	if area:
		self.__filter_contours_min_area = area
