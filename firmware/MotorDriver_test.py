import MotorDriver

dT = MotorDriver.MotorDriver()
dT.setDistance(100)
dT.setSpeed(20)
dT.setHeading(0)
dT.setTargetHeading(0)
dT.tmpSetDecision("none")
dT.move()
dT.motorStop()
