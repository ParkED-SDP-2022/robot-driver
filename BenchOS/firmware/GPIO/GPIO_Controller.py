import RPi.GPIO as GPIO
import time
 
class GPIO_Pins():
    
    def __init__(self):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
         
        #set GPIO Pins
        self.GPIO_TRIGGER_F = 17
        self.GPIO_ECHO_F= 23
        
        #set GPIO Pins
        self.GPIO_TRIGGER_FL = 18
        self.GPIO_ECHO_FL = 24
        
        #set GPIO Pins
        self.GPIO_TRIGGER_FR = 22
        self.GPIO_ECHO_FR = 25

        #set GPIO Pins
        self.GPIO_TRIGGER_B = 4
        self.GPIO_ECHO_B = 27
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER_B, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_B, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_FL, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_FL, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_FR, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_FR, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_F, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_F, GPIO.IN)    
    
#retriteve the forward US distance
    def distanceF(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER_F, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER_F, False)
     
        StartTime = time.time()
        StopTime = time.time()
        InitTime = time.time()
     
        # save StartTime
        while GPIO.input(self.GPIO_ECHO_F) == 0 and InitTime + 0.01 > StartTime:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_F) == 1 and StartTime + 0.01 > time.time:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        time.sleep(0.1)
        return distance    
    
    #retriteve the forward US distance
    def distanceFLeft(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER_FL, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER_FL, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(self.GPIO_ECHO_FL) == 0 and InitTime + 0.01 > StartTime:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_FL) == 1 and StartTime + 0.01 > time.time:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        time.sleep(0.1)
        return distance
    
    def distanceFRight(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER_FR, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER_FR, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(self.GPIO_ECHO_FR) == 0 and InitTime + 0.01 > StartTime:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_FR) == 1 and StartTime + 0.01 > time.time:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        time.sleep(0.1)
        return distance
    
    #retriteve the backward US distance
    def distanceBackward(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER_B, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER_B, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(self.GPIO_ECHO_B) == 0 and InitTime + 0.01 > StartTime:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_B) == 1 and StartTime + 0.01 > time.time:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        
        time.sleep(0.1)
        return distance
    
    def cleanup(self):
        print("Measurement stopped")
        GPIO.cleanup()
        return
