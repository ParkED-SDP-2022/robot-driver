import RPi.GPIO as GPIO
import time
 
class GPIO_Pins():
    
    def __init__(self):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
         
        #set GPIO Pins
        self.GPIO_TRIGGER_B = 17
        self.GPIO_ECHO_B = 23
        
        #set GPIO Pins
        self.GPIO_TRIGGER_FL = 18
        self.GPIO_ECHO_FL = 24
        
        #set GPIO Pins
        self.GPIO_TRIGGER_FR = 22
        self.GPIO_ECHO_FR = 25

        self.FSR_Pin1 = 4
        self.FSR_Pin2 = 5
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER_B, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_B, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_FL, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_FL, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER_FR, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_FR, GPIO.IN)


    def rc_time(FSR_Pin):
        count = 0

        # Output on the pin for
        GPIO.setup(FSR_Pin, GPIO.OUT)
        GPIO.output(FSR_Pin, GPIO.LOW)
        time.sleep(0.1)

        # Change the pin back to input
        GPIO.setup(FSR_Pin, GPIO.IN)

        # Count until the pin goes high
        while (GPIO.input(FSR_Pin) == GPIO.LOW):
            count += 1

        return count

         
         
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
        while GPIO.input(self.GPIO_ECHO_FL) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_FL) == 1:
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
        while GPIO.input(self.GPIO_ECHO_FR) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO_FR) == 1:
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
        
        time.sleep(0.1)
        return distance
    
    def cleanup(self):
        print("Measurement stopped")
        GPIO.cleanup()
        return
