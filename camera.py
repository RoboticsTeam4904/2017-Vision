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
# cameraResolution = (640, 480)
camera.nativeResolution = (2592, 1944)
camera.nativeAngle = (math.radians(53.5), math.radians(41.41))
camera.mountAngle = (0, math.radians(45))
camera.distToShooter = (13.25, 2.5)
camera.goalHeight = 8 * 12
camera.height = 296 / 25.4 #to inches

def getImage():
	image = None
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
	return image

# cnt = 1
# def getImage(webcam=False, useLatestImage=False, useStoredImage=False): # pi camera is default
# 	image = None
# 	if webcam:
# 		ret, image = cap.read()
# 		#cv2.imwrite("/Users/erik/"+str(time.time())+".jpg", image)
#
# 	elif useLatestImage:
# 		image = cv2.imread("latest.jpg")
#
# 	elif useStoredImage:
# 		cnt += 1
# 		print cnt
# 		image = cv2.imread("4/a{0:05d}.jpg".format(cnt))
# 		while(image == None and cnt < 10000):
# 			cnt += 1
# 			image = cv2.imread("4/a{0:05d}.jpg".format(cnt))
# 		if not cnt < 10000:
# 			cnt = 0
# 			image = getImage()
#
# 	else: # from pi camera
# 		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
# 			# grab the raw NumPy array representing the image, then initialize the timestamp
# 			# and occupied/unoccupied text
# 			image = frame.array
#
# 			# clear the stream in preparation for the next frame
# 			rawCapture.truncate(0)
# 	return image
