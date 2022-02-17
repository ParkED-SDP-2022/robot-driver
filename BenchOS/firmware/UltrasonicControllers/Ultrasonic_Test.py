from Ultrasonic import UltrasonicSensor
import time

uS = UltrasonicSensor()
# uS.setupForward()
# uS.setupBackward()

try:
    while True:
        print("Object "+str(uS.distanceForward())+"cm Forward")
        time.sleep(0.2)
        print("Object "+str(uS.distanceBackward())+"cm Backwards")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
