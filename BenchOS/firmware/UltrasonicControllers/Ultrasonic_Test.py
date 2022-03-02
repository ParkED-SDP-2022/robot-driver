from Ultrasonic import UltrasonicSensor
import time

uS = UltrasonicSensor()
# uS.setupForward()
# uS.setupBackward()

try:
    while True:
        print("Object "+str(uS.distanceForward())+"cm Forward")
        print("Object "+str(uS.distanceBackward())+"cm Backwards")

except KeyboardInterrupt as e:
    print("Measurement stopped by User: "+ e)
    GPIO.cleanup()
