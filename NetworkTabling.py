def initializeTables(center, calibrate=False):
	from networktables import NetworkTables
	NetworkTables.setTeam(team)
	NetworkTables.initialize(server=ip)

	# if calibrate:
		#pipeline.calibrate(hsv_threshold_hue=network.getNumber('hsv_threshold_hue'), hsv_threshold_saturation=network.getNumber('hsv_threshold_value'), hsv_threshold_value=network.getNumber('hsv_threshold_value'))

	return NetworkTables.getTable("SmartDashboard")

def publishToTables(debug, network, center, frameNum=0, distance=0):
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
