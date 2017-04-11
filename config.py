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
displacement = 4.25/12.0 # Vertical feet from camera to bottom of vision target
cameraTilt = 0 # REORGANIZE CONSTANTS INTO APPROPRIATE FILES
width = 8.25/12.0 #from centers. targets are 2x5 inches and 6.25 inches apart
nativeAngle  = (np.radians(64), np.radians(48)) #experimentally determined 10 pxl per deg at 640x480, going down by a v smol amount at the edge of the frame
def setResolution(res): # REMOVE NEW FUNCTION
	global resolution, degPerPxl
	resolution = res
	degPerPxl = np.divide(nativeAngle, resolution)
setResolution((640, 480))

# Misc
# -------------
withOpenCV3 = int(cv2.__version__[0]) == 3
sampleImage = "TestImages/GearTest.png"

