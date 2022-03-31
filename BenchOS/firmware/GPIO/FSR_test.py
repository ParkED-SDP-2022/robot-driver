import time
import grovepi
 
# Connect the Grove Slide Potentiometer to analog port A0
# OUT,LED,VCC,GND
slide = 0   # pin 1 (yellow wire)
 
# The device has an onboard LED accessible as pin 2 on port A0
# OUT,LED,VCC,GND
led = 1     # pin 2 (white wire)
 
grovepi.pinMode(slide,"INPUT")
grovepi.pinMode(led,"OUTPUT")
time.sleep(1)
 
while True:
    try:
        # Read sensor value from potentiometer
        sensor_value = grovepi.analogRead(slide)
 
        # Illuminate onboard LED
        if sensor_value > 500:
            print("bench occupied")
        else:
            print("bench empty")
 
        print "sensor_value =", sensor_value
 
    except IOError:
        print "Error"
