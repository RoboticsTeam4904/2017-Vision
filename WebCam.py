import cv2
import subprocess
camera = cv2.VideoCapture(0)

def getImage():
	subprocess.call("/usr/bin/v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_auto_priority=0 -c exposure_absolute=18 -c gain=10 -c contrast=40", shell=True)
	retval, image = camera.read()
	return image

def set(resolution=False, exposure=False):
	if resolution:
		camera.set(3, resolution[0])
		camera.set(4, resolution[1])
	if exposure:
		subprocess.call("/usr/bin/v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_auto_priority=0 -c exposure_absolute="+str(exposure)+" -c gain=10 -c contrast=40", shell=True)

def getExposure():
	return camera.get(15)
