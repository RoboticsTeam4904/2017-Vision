import cv2
# Logging/debug settings
# --------------
debug = True
extra_debug = False #step through each contour in the webcam by turning on extra_debug
save = False
display = True

# Camera settings
# --------------
exposure = 15
gain = 10
contrast = 50
degPerPxl = 0.1 #experimentally determined 10 pxl per deg, going down by a v smol amount at the edge of the frame
displacement = (6.5 + 5)/12.0 # Vertical feet from camera to bottom of vision target + Height of target in feet
cameraTilt = 0
width = 8.25/12 #from centers. targets are 2x5 inches and 6.25 inches apart
resolution = (640, 360)

# Misc
# -------------
ip = "10.49.4.2"
team = 4904
withOpenCV3 = int(cv2.__version__[0]) == 3
edited = False
sampleImage = "TestImages/GearTest.png"