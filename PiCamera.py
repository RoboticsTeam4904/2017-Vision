def getPiImage(camera):
	return camera.getImage()

def initializePiCamera(resolution):
	import camera
	camera.camera.resolution = resolution
	return camera
