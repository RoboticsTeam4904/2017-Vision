import cv2, subprocess, SpikeFinding
import numpy as np

exposure = 3
gain = 10
contrast = 50
camera = cv2.VideoCapture(0)

def getImage():
	retval, image = camera.read()
	return image


def fireBlanks(numBlanks=3):
	for i in range(numBlanks):
		getImage()

def reloadTime(duration=30): #in miliseconds
	cv2.waitkey(duration)

def setRealExposure(exposure):
	setCamera(exposure=exposure)
	reloadTime()
	fireBlanks()

def setCamera(resolution=False, exposure=False, gain=False, contrast=False):
	settingStr = "/usr/bin/v4l2-ctl -d /dev/video0"
	if resolution:
		settingStr += " --set-fmt-video=width={},height={}".format(resolution[0], resolution[1])
	if exposure:
		settingStr += " -c exposure_auto=1 -c exposure_auto_priority=0 -c exposure_absolute={}".format(exposure)
	if gain:
		settingStr += " -c gain={}".format(gain)
	if contrast:
		settingStr += " -c contrast={}".format(contrast)
	subprocess.call(settingStr, shell=True)
	if resolution:
		SpikeFinding.resolution = resolution # Perhaps getResolution is safer?
		SpikeFinding.degPerPxl = np.divide(SpikeFinding.nativeAngle, resolution)

def getExposure():
	return int(subprocess.check_output("/usr/bin/v4l2-ctl -d /dev/video0 -C exposure_absolute", shell=True)[19:].strip())

def getResolution():
	resolution = getImage().shape
	return resolution[1], resolution[0]

setCamera(resolution=SpikeFinding.resolution, exposure=exposure, gain=gain, contrast=contrast)
if config.debug:
	print "Exposure: ", WebCam.getExposure()
