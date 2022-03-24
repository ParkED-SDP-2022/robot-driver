import time
from GPIO_Controller import GPIO_Pins

uS = GPIO_Pins()
# uS.setupForward()
# uS.setupBackward()

try:
    while True:
        
        print("Object "+str(uS.distanceF())+"cm Forward")
        print("Object "+str(uS.distanceFLeft())+"cm ForwardLeft")
        print("Object "+str(uS.distanceFRight())+"cm ForwardRight")
        print("Object "+str(uS.distanceBackward())+"cm Backwards")

except KeyboardInterrupt as e:
    print("Measurement stopped by User: "+ str(e))
    GPIO.cleanup()
