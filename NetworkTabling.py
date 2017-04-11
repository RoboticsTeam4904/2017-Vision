from networktables import NetworkTables
import config

ip = "10.49.4.2"
team = 4904

NetworkTables.setTeam(team)
NetworkTables.initialize(server=ip)

table = NetworkTables.getTable("Vision")

def publishToTables(isVisible=True, angleToGoal=0, distance=0, frameNum=0):
	table.putBoolean('trustable', isVisible)
	table.putNumber('degrees', angleToGoal)
	table.putNumber('distance', distance)
	table.putNumber('frameNum', frameNum)

def checkForCalibrate():
	return table.getBoolean('Autocalibration', False)

def putCalibrated():
	table.putBoolean('Autocalibration complete', True)
	table.putBoolean('Autocalibration', False)
