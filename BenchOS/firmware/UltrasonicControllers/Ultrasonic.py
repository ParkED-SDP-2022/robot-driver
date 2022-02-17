import RPi.GPIO as GPIO
import time
 
 
class UltrasonicSensor():
    
    def __init__(self):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
         
        #set GPIO Pins
        self.GPIO_TRIGGER_B = 17
        self.GPIO_ECHO_B = 23
        
        #set GPIO Pins
        self.GPIO_TRIGGER_F = 18
        self.GPIO_ECHO_F = 24
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER_B, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_B, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_F, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_F, GPIO.IN)
         
         
         
    #retriteve the forward US distance
    def distanceForward(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER_F, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER_F, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(self.GPIO_ECHO_F) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_F) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
     
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
        while GPIO.input(self.GPIO_ECHO_B) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_B) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        
        return distance
    
    def cleanup(self):
        print("Measurement stopped")
        GPIO.cleanup()
        return