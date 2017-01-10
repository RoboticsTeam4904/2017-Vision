from __future__ import division #Might take time to import
import math
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=camera.resolution)
#camera.start_preview()
camera.exposure_mode = 'sports'

# constants
camera.nativeResolution = (2592, 1944)
camera.nativeAngle = (math.radians(53.5), math.radians(41.41))
camera.mountAngle = (0, math.radians(45))
camera.distToShooter = (13.25, 2.5)
camera.goalHeight = 8 * 12
camera.height = 296 / 25.4 #to inches

def getImage():
	# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = camera.capture(rawCapture, format="bgr", use_video_port=True):

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	return frame.array
