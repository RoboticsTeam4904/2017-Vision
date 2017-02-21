from networktables import NetworkTables
from autocalibrate import calibrate
NetworkTables.initialize(server='10.49.4.2')
table = NetworkTables.getTable('autocalibrate')

calibrations = 10000

print "starting!"
while True:
	foo = table.getNumber('autocalibrate', -1)
	print "foo is ", foo
	if foo > calibrations:
		print "For some reason, we are calibrating the camera"
		calibrations += 1
		calibrate()
		table.putBoolean('didCalibrate', True)

