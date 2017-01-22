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
