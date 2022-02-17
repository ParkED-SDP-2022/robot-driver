import Ultrasonic

uS = Ultrasonic()

print(uS.distanceForward())

print(uS.distanceBackward())

uS.shutdown()