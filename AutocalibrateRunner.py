from networktables import NetworkTables
from autocalibrate import calibrate
NetworkTables.initialize(server='tegra-ubuntu.local')
table = NetworkTables.getTable('autocalibrate')

calibrations = 0


while True:
	foo = table.getNumber('autocalibration', True)
	if foo > calibrations:
		calibrations += 1
		calibrate()
