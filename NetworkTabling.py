from networktables import NetworkTables
from config import team, ip, halfWidth

NetworkTables.setTeam(team)
NetworkTables.initialize(server=ip)

table = NetworkTables.getTable("Vision")

def publishToTables(isVisible=True, angleToGoal=0, distance=0, frameNum=0):
	table.putBoolean('trustable', isVisible)
	table.putNumber('degrees', angleToGoal)
	table.putNumber('distance', distance)
	table.putNumber('frameNum', frameNum)

def calibrateFromTables():
	import GripRunner
	GripRunner.calibrate(hsv=[[table.getNumber('hsv_threshold_hue_bottom'), table.getNumber('hsv_threshold_hue_top')], [table.getNumber('hsv_saturation_value_bottom'), table.getNumber('hsv_saturation_value_top')], [table.getNumber('hsv_threshold_value_bottom'), table.getNumber('hsv_threshold_value_top')]])
