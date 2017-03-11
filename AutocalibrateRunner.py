from networktables import NetworkTables
from autocalibrate import calibrate
import config
NetworkTables.setTeam(config.team)
NetworkTables.initialize(server=config.ip)
table = NetworkTables.getTable('Vision')

calibrations = 0
while True:
	robotPresses = table.getNumber('Autocalibration count', -1)
	if robotPresses > calibrations:
		print "Calibrating the camera due to button press"
		calibrations += 1
		calibrate()

