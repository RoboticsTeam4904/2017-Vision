import re,  config

# This code was not what we planned to write; in fact, we still cringe at its sight
# But, seeing how our code is a little rudamentary, we are forced to add some artificial intelligence.
# Sadly, we have written code that transcends programming itself. This code writes its own code.
# This horrid beast has taken our jobs and our enthusiasm. If we never code again, know it was because of this function.
# So Team 4904 presents you the next level of programming:
code = open('gears.py', 'r').read()
if config.withOpenCV3:
	code = re.sub('    contours, hierarchy =cv2.findContours', '    im2, contours, hierarchy =cv2.findContours', code)
else:
	code = re.sub('im2, contours, hierarchy =cv2.findContours', 'contours, hierarchy =cv2.findContours', code)
open('gears_edited.py', 'w').write(code)

from grip_edited import GripPipeline
pipeline = GripPipeline()

def run(image):
	pipeline.process(image)
	return pipeline.filter_contours_output
