from picamera.array import PiRGBArray
from picamera import PiCamera
camera = PiCamera()

def getImage():
	rawCapture = PiRGBArray(camera, size=camera.resolution)
	camera.capture(rawCapture, format="bgr", use_video_port=True)
	return rawCapture.array

def set(resolution=False, exposure=False, exposure_mode=False, shutter_speed=False): #e.g. 'snow'
	global rawCapture
	rawCapture = PiRGBArray(camera, size=camera.resolution)
	if resolution:
		camera.resolution = resolution
	if exposure:
		pass
	if shutter_speed:
		camera.shutter_speed = shutter_speed
	if exposure_mode:
		camera.exposure_mode = exposure

	# camera.brightness = 0 to 100 # default 50
	# camera.contrast = -100 to 100 # default 0
	# camera.saturation = -100 to 100 # default 0
	# camera.exposure_compensation = -25 to 25 # default 0
	# camera.contrast = -100 to 100 # default 0
	# camera.image_effect - various effects

def getShutterSpeed():
	return camera.shutter_speed


#camera.start_preview()

# Constants
# camera.nativeResolution = (2592, 1944)
# camera.nativeAngle = (math.radians(53.5), math.radians(41.41))
# camera.mountAngle = (0, math.radians(45))
# camera.distToShooter = (13.25, 2.5)
# camera.goalHeight = 8 * 12
# camera.height = 296 / 25.4 #to inches

