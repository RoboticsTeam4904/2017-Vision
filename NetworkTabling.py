from networktables import NetworkTables

team = 4904
ip = "10.49.4.2"

NetworkTables.setTeam(team)
NetworkTables.initialize(server=ip)
table = NetworkTables.getTable("SmartDashboard")


def publishToTables(center, frameNum=0, distance=0, halfWidth):
	isVisible = False
	if center:
		isVisible = True
		if adjustCoords:
			center[0] = center[0] - halfWidth
	else:
		isVisible = False
		center = (0,0)
	table.putNumber('centerX', center[0])
	table.putNumber('centerY', center[1]) # Can be deleted
	table.putBool('isVisible', isVisible)
	table.putNumber('frameNum', frameNum)
	table.putNumber('distance', distance) # Feet away

	# if debug:
		# print "Published to network tables."

def calibrateFromTables():
	import GripRunner
	GripRunner.calibrate(hsv=[[table.getNumber('hsv_threshold_hue_bottom'), table.getNumber('hsv_threshold_hue_top')], [table.getNumber('hsv_saturation_value_bottom'), table.getNumber('hsv_saturation_value_top')], [table.getNumber('hsv_threshold_value_bottom'), table.getNumber('hsv_threshold_value_top')]])

