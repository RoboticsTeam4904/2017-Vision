import cv2
import numpy as np
# Logging/debug settings
# --------------
debug = False
extra_debug = False #step through each contour in the webcam by turning on extra_debug
display = False
save = True
saveFrequency = 50

# Misc
# -------------
withOpenCV3 = int(cv2.__version__[0]) == 3
