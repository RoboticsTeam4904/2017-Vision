import time, config

NetworkTables.setTeam(config.team)
NetworkTables.initialize(server=config.ip)
table = NetworkTables.getTable("Test")
delay = 100
i = 1
while True:
	while True:
		if table.getBoolean("Failed"):
			print "failed with delay: ", delay
			break
		table.putNumber(i)
		i += 1
		print i
		time.sleep(delay)
	delay -= 10
	table.putBoolean("Failed", False)