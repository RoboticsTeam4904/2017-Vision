# Logging/debug settings
# --------------
debug = False
#step through each contour in the webcam by turning on extra_debug
extra_debug = False
save = False
display = False

# Camera settings
# --------------
exposure = 30
gain = 10
contrast = 50
resolution = (640, 360)
heightFromAFoot = 272#/(1944/resolution[1])

cameraHeight = 12 #inches
nativeAngleY = 0.83 # not sure
nativeAngleX = 1.1 # 63
#experimentally determined 10 pxl per deg, going down by a v smol amount at the edge of the frame
degPerPxl = 0.1

# Misc
# -------------
ip = "10.49.4.2"
team = 4904
withOpenCV3 = True
edited = False
sampleImage = "TestImages/GearTest.png"
