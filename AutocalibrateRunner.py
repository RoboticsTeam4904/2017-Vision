from NetworkTabling import table
from autocalibrate import calibrate
import config

while True:
	if table.getBoolean('Autocalibration', False):
		print "Calibrating the camera due to button press"
		calibrate()
		table.putBoolean('Autocalibration complete', True)
		table.putBoolean('Autocalibration', False)
