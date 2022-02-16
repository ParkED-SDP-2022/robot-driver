from motors import Motors 
from time import time, sleep 

class MotorDriver()
    
    def __init__():
        mc = Motors() 
        run_time = 5        # number of seconds to run motors 
        MotorLeft = [0, 1, 2]
        MotorRight = [3, 4, 5]
        targetDistance = 0
        turningAngle = 0
        drivingSpeed = 0
    
    def forwardspd(self, spd):
        print("Driving Forward & spd:"+str(spd))
        for i in MotorLeft:
            mc.move_motor(i, spd)
        for i in MotorRight:
            mc.move_motor(i, -spd)
        run_time = 1
        encoderOut(run_time)
        return

    def turnAngular(self, angle, spd):
        if angle < 0:
            print("Turning right")
            for i in MotorLeft:
                mc.move_motor(i, -spd*angle*0.1)
            for i in MotorRight:
                mc.move_motor(i, spd*angle*0.1)
            run_time = 1
            encoderOut(run_time)
        if angle > 0:
            print("Turning left")
            for i in MotorLeft:
                mc.move_motor(i, spd*angle*0.1)
            for i in MotorRight:
                mc.move_motor(i, -spd*angle*0.1)
            run_time = 1
            encoderOut(run_time)
        return

    def encoderOut(self, run_time):
    # Encoder board can be fragile - always use a try/except loop
        start_time = time()
        while time() < start_time + run_time:
            try:
              mc.print_encoder_data() 
              sleep(0.2)     # Use a sleep of at least 0.1, to avoid errors
            except:
                print("encoderError")
        return
          
    def motorStop(self):
        mc.stop_motors() 
    
    
    def setDistance(self, distance):
        targetDistance = distance
    def setSpeed(self, speed):
        drivingSpeed = speed
    def setAngle(self, angle):
        turningAngle = angle
    def getEncoderData():
        try:
            mc.print_encoder_data() 
        except:
            print("encoderError")
            
            
    def main():
        for i in range(0,2,1):
            
            forwardspd(20)
            sleep(1)
            turnAngular(10,20)
            sleep(1)
            motorStop()
