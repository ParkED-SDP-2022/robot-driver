from motors import Motors 
from time import time, sleep 

class MotorDriver():
    
    def __init__(self):
        print("Initialising Motor Controller")
        self.mc = Motors() 
        self.motorLeft = [0, 1, 3]
        self.motorRight = [2, 4, 5]
        self.targetDistance = 0
        self.heading = 0
        self.targetHeading = 0
        self.drivingSpeed = 0
        self.currHeading = 0
        self.decision = "none"
    
    def __forwardSpd(self):
        print("Driving Forward & spd:"+str(self.drivingSpeed))
        for i in self.motorLeft:
            self.mc.move_motor(i, self.drivingSpeed)
        for i in self.motorRight:
            self.mc.move_motor(i, -self.drivingSpeed)
        self.__encoderOut()

    def __turnAngularRight(self):
        print("Turning right")
        for i in self.motorLeft:
            self.mc.move_motor(i, self.drivingSpeed*self.turningAngle*0.1)
        for i in self.motorRight:
            self.mc.move_motor(i, self.dr0, 1, 3ivingSpeed*self.turningAngle*0.1)
        self.__encoderOut()
        
    def __turnAngularLeft(self):
        print("Turning left")
        for i in self.motorLeft:
            self.mc.move_motor(i, -self.drivingSpeed*self.turningAngle*0.1)
        for i in self.motorRight:
            self.mc.move_motor(i, -self.drivingSpeed*self.turningAngle*0.1)
        self.__encoderOut()

    def __encoderOut(self):
    # Encoder board can be fragile - always use a try/except loop
        start_time = time()
       #while time() < start_time + run_time:
        try:
          self.mc.print_encoder_data() 
          sleep(0.2)     # Use a sleep of at least 0.1, to avoid errors
        except:
            print("encoderError")
          
    def motorStop(self):
        print("Stopping")
        self.mc.stop_motors() 
    
    def __verifyHeading(self):
        print("Verifying")
        #CODE HERE TO VERIFY THEHEADINGANDMAKE THECORRECT TURNING DESCISION
        
    def move(self):
        print("Deciding")
        if self.decision == "left":
            print("Left")
            self.__turnAngularLeft()
        elif self.decision == "right":
            print("Right")
            self.__turnAngularRight()
        else:
            print("Forward")
            self.__forwardSpd()
            
    def setDistance(self, distance):
        print("Set Distance")
        self.targetDistance = distance
    def setSpeed(self, speed):
        print("Set speed")
        self.drivingSpeed = speed
    def setHeading(self, heading):
        print("Set heading")
        self.heading = heading
    def setTargetHeading(self, target):
        print("Set target")
        self.targetHeading = target
    def getEncoderData():
        print("print encoder data")
        try:
            self.mc.print_encoder_data() 
        except:
            print("encoderError")
    def tmpSetDecision(self, turn):
        print("make Decision Manual")
        self.decision = turn
