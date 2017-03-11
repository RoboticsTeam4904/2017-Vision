from networktables import NetworkTables
from autocalibrate import calibrate
from config import ip, team
NetworkTables.setTeam(team)
NetworkTables.initialize(server=ip)
table = NetworkTables.getTable('autocalibrate')

calibrations = 0

print "Starting Button Autocalibration!"
while True:
	robotPresses = table.getNumber('autocalibrate', -1)
	print "robotPresses is ", robotPresses
	if robotPresses > calibrations:
		print "For some reason, we are calibrating the camera"
		calibrations += 1
		calibrate()
		table.putBoolean('didCalibrate', True)

