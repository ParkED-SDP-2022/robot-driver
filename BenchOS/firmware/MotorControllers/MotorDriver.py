from motors import Motors 
from time import time, sleep
from CompassController.Compass import compass

class MotorDriver():
    
    def __init__(self):
        print("Initialising Motor Controller")
        self.mc = Motors() 
        self.motorLeft = [0, 2, 5]
        self.motorRight = [1, 4, 2]
        self.naturalDirection = [1,1,1,1,1,1]
        self.targetDistance = 0
        self.heading = 0
        self.update = False
        self.targetHeading = 0
        self.drivingSpeed = 0
        self.currHeading = 0
        self.decision = "none"
        self.turningAngle = 0
        self.leftAngular = 0
        self.rightAngular = 0
        self.compass = CompassData()
    
    #private method will drive the robot at a speed set by the interface
    #the angular will be set by the offset in heading and affect the speed
    #of each motor to enable long arcing turns or on the spot turns
    def __moveSpd(self):
        print("Driving Forward & spd:"+str(self.drivingSpeed))

        while self.update:
            self.__setHeading(self.compass.getHeading())
            self.__verifyHeading()
            # driving the bench forward with variable turning
            if self.drivingSpeed >= 0:
                for i in self.motorLeft:
                    self.mc.move_motor(i, self.drivingSpeed*(self.leftAngular+1)*(-self.rightAngular+1))
                for i in self.motorRight:
                    self.mc.move_motor(i, -self.drivingSpeed*(-self.leftAngular+1)*(self.rightAngular+1))
                self.__encoderOut()
            
            #reversing controls are reveresed
            else:
                for i in self.motorLeft:
                    self.mc.move_motor(i, -self.drivingSpeed*(-self.leftAngular+1)*(self.rightAngular+1))
                for i in self.motorRight:
                    self.mc.move_motor(i, self.drivingSpeed*(self.leftAngular+1)*(-self.rightAngular+1))
                self.__encoderOut()
        

    def __encoderOut(self):
    # Encoder board can be fragile - always use a try/except loop
        start_time = time()
       #while time() < start_time + run_time:
        try:
          self.mc.print_encoder_data() 
          sleep(0.5)     # Use a sleep of at least 0.1, to avoid errors
        except:
            print("encoderError")
          
    def motorStop(self):
        print("Stopping")
        self.update = False
        self.mc.stop_motors() 
    
    def __verifyHeading(self):
        #verify the heading and assign the angular speed
        print("Verifying")
        if self.heading - self.targetHeading < -180:
            self.targetHeading - 180
        elif self.heading - self.targetHeading > 180:
            self.targetHeading + 180
        self.__angleResolution()
                                   
    def __angleResolution(self):
        self.turningAngle = self.heading - self.targetHeading
        self.leftAngular = self.turningAngle/2
        self.rightAngular = self.turningAngle/2
        self.__moveSpd()
            
            
    def move(self):
        self.setGo = True
        self.__moveSpd()

#-----------------------------------------------------------------------------------------------------
    # getter and setters below
            
    def setDistance(self, distance):
        print("Set Distance")
        self.targetDistance = distance
                                   
    def setSpeed(self, speed):
        print("Set speed")
        self.drivingSpeed = speed
                                   
    def __setHeading(self, heading):
        print("Set heading")
        self.heading = heading
                                   
    def setTargetHeading(self, target):
        print("Set target")
        self.targetHeading = target
    
    #Test only function
    def setTurningAngle(self, angle):
        self.turningAngle = angle
        self.__angleResolution()
        
                                   
    def getEncoderData():
        print("print encoder data")
        try:
            self.mc.print_encoder_data() 
        except:
            print("encoderError")
        
    def motorTest(self):
        for i in range(0,6,1):
            self.mc.move_motor(i, 100*self.naturalDirection[i])
            run_time = 4
            strtTime = time()
            while time()< strtTime + run_time:
                print(str(i))
                self.__encoderOut()
            self.motorStop()
        