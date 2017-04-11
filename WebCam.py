import cv2, subprocess
import numpy as np

exposure = 90
gain = 10
contrast = 50
nativeAngle  = (np.radians(64), np.radians(48)) #experimentally determined 10 pxl per deg at 640x480, going down by a v smol amount at the edge of the frame
resolution = (640, 480)
degPerPxl = np.divide(nativeAngle, resolution)

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

def setCamera(cameraResolution=False, exposure=False, gain=False, contrast=False):
	settingStr = "/usr/bin/v4l2-ctl -d /dev/video0"
	if cameraResolution:
		settingStr += " --set-fmt-video=width={},height={}".format(cameraResolution[0], cameraResolution[1])
	if exposure:
		settingStr += " -c exposure_auto=1 -c exposure_auto_priority=0 -c exposure_absolute={}".format(exposure)
	if gain:
		settingStr += " -c gain={}".format(gain)
	if contrast:
		settingStr += " -c contrast={}".format(contrast)
	subprocess.call(settingStr, shell=True)
	if cameraResolution:
		global resolution, degPerPxl
		resolution = cameraResolution
		degPerPxl = np.divide(nativeAngle, cameraResolution)

def getExposure():
	return int(subprocess.check_output("/usr/bin/v4l2-ctl -d /dev/video0 -C exposure_absolute", shell=True)[19:].strip())

def getResolution():
	resolution = getImage().shape
	return resolution[1], resolution[0]

setCamera(cameraResolution=resolution, exposure=exposure, gain=gain, contrast=contrast)
