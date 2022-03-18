from Compass import CompassData
import time

comp = CompassData()
try:
    while True:
        print(" Heading: "+ str(comp.getHeading()))

except KeyboardInterrupt as e:
    print("Measurement stopped by User: "+ e)
    GPIO.cleanup()
