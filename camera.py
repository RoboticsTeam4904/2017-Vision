from __future__ import division #Might take time to import
import math
from picamera.array import PiRGBArray
from picamera import PiCamera

Camera = PiCamera()
Camera.resolution = (640, 480)
Camera.framerate = 5
rawCapture = PiRGBArray(Camera, size=Camera.resolution)
#Camera.start_preview()
Camera.exposure_mode = 'sports'

# constants
Camera.nativeResolution = (2592, 1944)
Camera.nativeAngle = (math.radians(53.5), math.radians(41.41))
Camera.mountAngle = (0, math.radians(45))
Camera.distToShooter = (13.25, 2.5)
Camera.goalHeight = 8 * 12
Camera.height = 296 / 25.4 #to inches

def getImage():
	# for frame in Camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = Camera.capture(rawCapture, format="bgr", use_video_port=True):

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	return frame.array
