from __future__ import division #Might take time to import
import math
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 360)

# Settings and Preferences
camera.shutter_speed = 5  # camera.exposure_speed (if shutter_speed not set, it will read the auto shutter_speed)
camera.framerate = 30
camera.exposure_mode = 'snow'
# camera.brightness = 0 to 100 # default 50
# camera.contrast = -100 to 100 # default 0
# camera.saturation = -100 to 100 # default 0
# camera.exposure_compensation = -25 to 25 # default 0
# camera.contrast = -100 to 100 # default 0
# camera.image_effect - various effects

#camera.start_preview()

# Constants
# camera.nativeResolution = (2592, 1944)
# camera.nativeAngle = (math.radians(53.5), math.radians(41.41))
# camera.mountAngle = (0, math.radians(45))
# camera.distToShooter = (13.25, 2.5)
# camera.goalHeight = 8 * 12
# camera.height = 296 / 25.4 #to inches

def getImage():
	# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	rawCapture = PiRGBArray(camera, size=camera.resolution)
	frame = camera.capture(rawCapture, format="bgr", use_video_port=True)
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	return frame.array

def read():
	return True, getImage()