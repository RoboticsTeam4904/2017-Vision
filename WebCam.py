import cv2
import subprocess
camera = cv2.VideoCapture(0)

def getImage():
	retval, image = camera.read()
	return image

def set(resolution=False, exposure=False, gain=False, contrast=False):
	if resolution:
		camera.set(3, resolution[0])
		camera.set(4, resolution[1])
	if exposure:
		subprocess.call("/usr/bin/v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_auto_priority=0 -c exposure_absolute={}".format(exposure), shell=True)
	if gain:
		subprocess.call("/usr/bin/v4l2-ctl -d /dev/video0 -c gain={}".format(gain), shell=True)
	if contrast:
		subprocess.call("/usr/bin/v4l2-ctl -d /dev/video0 -c contrast={}".format(contrast), shell=True)



def getExposure():
	return int(subprocess.check_output("/usr/bin/v4l2-ctl -d /dev/video0 -C exposure_absolute", shell=True)[19:].strip())
