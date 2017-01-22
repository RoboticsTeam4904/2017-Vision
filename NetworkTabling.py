def initializeTables(center, calibrate=False):
	from networktables import NetworkTables
	NetworkTables.setTeam(team)
	NetworkTables.initialize(server=ip)
	return NetworkTables.getTable("SmartDashboard")

def publishToTables(network, center, frameNum=0, distance=0):
	isVisible = False
	if center:
		isVisible = True
		if adjustCoords:
			center[0] = center[0] - halfWidth
	else:
		isVisible = False
		center = (0,0)
	sd.putNumber('centerX', center[0])
	sd.putNumber('centerY', center[1]) # Can be deleted
	sd.putBool('isVisible', isVisible)
	sd.putNumber('frameNum', frameNum)
	sd.putNumber('distance', distance) # Feet away


	if debug:
		print "Published to network tables."

def calibrateFromTables():
	import GripRunner
	GripRunner.calibrate(hsv=[[network.getNumber('hsv_threshold_hue_bottom'), network.getNumber('hsv_threshold_hue_top')], [network.getNumber('hsv_saturation_value_bottom'), network.getNumber('hsv_saturation_value_top')], [network.getNumber('hsv_threshold_value_bottom'), network.getNumber('hsv_threshold_value_top')]])

