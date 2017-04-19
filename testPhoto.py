import PiCamera, Printing, GripRunner, ContourFinding, SpikeFinding, autocalibrate
n = 0
def d():
	while True:
		o()

def s():
	global n
	image = PiCamera.getImage()
	Printing.save(image, name="TEST" + str(n))
	n += 1

def e(exposure):
	PiCamera.setCamera(shutter_speed=exposure)

def o():
	image = PiCamera.getImage()
	contours = GripRunner.run(image)
	targets = ContourFinding.filterContoursByArea(contours) # To be edited if the last filter is changed in case of algorithmic changes.
	# center, distance = SpikeFinding.findCenterandDist(targets) #if 2, join and find center, if 1, return val, if 0 return input. if adjustCoords:	center[0] -= halfWidth
	# # Printing.printResults(contours, center, distance)
	Printing.drawImage(image, contours, targets)
	Printing.display(image)
