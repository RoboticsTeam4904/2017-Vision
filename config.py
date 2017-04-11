import cv2
import numpy as np
# Logging/debug settings
# --------------
debug = False
extra_debug = False #step through each contour in the webcam by turning on extra_debug
display = False
save = True
saveFrequency = 50

# Camera settings
# --------------
exposure = 90
gain = 10
contrast = 50
nativeAngle  = (np.radians(64), np.radians(48)) #experimentally determined 10 pxl per deg at 640x480, going down by a v smol amount at the edge of the frame
resolution = (640, 480)
degPerPxl = np.divide(nativeAngle, resolution)

# Misc
# -------------
withOpenCV3 = int(cv2.__version__[0]) == 3
