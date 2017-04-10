from picamera.array import PiRGBArray
from picamera import PiCamera
camera = PiCamera()

def getImage():
	rawCapture = PiRGBArray(camera, size=camera.resolution)
	camera.capture(rawCapture, format="bgr", use_video_port=True)
	return rawCapture.array

def set(resolution=False, exposure=False, exposure_mode=False, shutter_speed=False): #e.g. 'snow'
	if resolution:
		camera.resolution = resolution
	if shutter_speed:
		camera.shutter_speed = shutter_speed
	if exposure_mode:
		camera.exposure_mode = exposure
	if resolution:
		config.setResolution(getResolution())

	# camera.brightness = 0 to 100 # default 50
	# camera.contrast = -100 to 100 # default 0
	# camera.saturation = -100 to 100 # default 0
	# camera.exposure_compensation = -25 to 25 # default 0
	# camera.contrast = -100 to 100 # default 0
	# camera.image_effect - various effects

def getShutterSpeed():
	return camera.shutter_speed

def getResolution():
	resolution = getImage().shape
	return resolution[1], resolution[0]

