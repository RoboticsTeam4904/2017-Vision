import cv2
import subprocess
camera = cv2.VideoCapture(0)

def getImage():
	retval, image = camera.read()
	return image

def set(resolution=False, exposure=False):
	if resolution:
		camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
		#camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, resolution[0])
		#camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, resolution[1])
		camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 360)
	camera.set(cv2.cv.CV_CAP_PROP_FPS, 60)
	#if exposure:
	#	subprocess.call("/usr/bin/v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_auto_priority=0 -c exposure_absolute="+str(exposure)+" -c gain=10 -c contrast=50", shell=True)

def getExposure():
	return camera.get(15)
