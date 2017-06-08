from networktables import NetworkTables
import config, Camera.autocalibrate

ip = "10.49.4.2"
team = 4904
isVisibleKey, angleKey, distanceKey, frameNumKey = 'trustable', 'degrees', 'distance', 'frameNum' #make key organization better

NetworkTables.setTeam(team)
NetworkTables.initialize(server=ip)
table = NetworkTables.getTable("Vision")

def publishToTables(isVisible=True, angleToGoal=0, distance=0, frameNum=0):
	table.putBoolean(isVisibleKey, isVisible)
	table.putNumber(angleKey, angleToGoal)
	table.putNumber(distanceKey, distance)
	table.putNumber(frameNumKey, frameNum)

def checkForCalibrate():
	return 

def calibrateIfButton():
	if table.getBoolean('Autocalibration', False):
		print "CALIBRATING the camera due to button press"
		Autocalibrate.calibrate()
		putCalibrated()

def putCalibrated():
	table.putBoolean('Autocalibration complete', True)
	table.putBoolean('Autocalibration', False)
