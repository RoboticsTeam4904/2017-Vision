# Logging/debug settings
# --------------
debug = True
#step through each contour in the webcam by turning on extra_debug
extra_debug = False
save = False
display = True

# Camera settings
# --------------
exposure = 12
gain = 10
contrast = 50
resolution = (640, 360)
halfWidth = resolution[0]/2
heightFromAFoot = 272#/(1944/resolution[1])

cameraHeight = 12 #inches
nativeAngleY = 0.7 # 57 degrees
nativeAngleX = 1.26 # undetermined
# 16:9, 72.34x40.69
# 4:3, 49.88, 63.6



# Misc
# -------------
ip = "10.49.4.2"
team = 4904
withOpenCV3 = False
edited = False
sampleImage = "TestImages/GearTest.png"
