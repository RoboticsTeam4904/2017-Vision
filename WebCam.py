import cv2
import subprocess
camera = cv2.VideoCapture(0)

def getImage():
	retval, image = camera.read()
	return image

def set(resolution=False, exposure=False, gain=False, contrast=False):
	settingStr = "/usr/bin/v4l2-ctl -d /dev/video0"
	if resolution:
		camera.set(3, resolution[0])
		camera.set(4, resolution[1])
	if exposure:
		settingStr += " -c exposure_auto=1 -c exposure_auto_priority=0 -c exposure_absolute={}".format(exposure)
	if gain:
		settingStr += " -c gain={}".format(gain)
	if contrast:
		settingStr += " -c contrast={}".format(contrast)
	subprocess.call(settingStr, shell=True)	



def getExposure():
	return camera.get(15)
