#!/usr/bin/env python
import imp
import rospy
import numpy as np
from std_msgs.msg import String
import json
import time
import GPIO
from BenchOS.firmware.MotorControllers.MotorDriver import MotorDriver
from BenchOS.firmware.UltrasonicControllers.Ultrasonic import UltrasonicSensor

class BigTest():
    def __init__(self):
        
        self.uS = UltrasonicSensor()
        self.mD = MotorDriver()

        motorListener = subprocess.Popen(["rosrun", "robot-driver", "cmd_vel_test.py"])
        
        rospy.init_node('firmwareTest', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", String, self.callback)

    def callback(self, data):
        print("The config is", data.data)
        self.parse(json.loads(data.data))
    
    def parse(self, raw_data):
        x = raw_data['x']
        y = raw_data['y']
        
        if uS.distanceForward() < 10 && x > 0:
            self.md.motorStop()
        elif uS.distanceBackward() < 10 && x < 0:
            self.md.motorStop()
        else:
            self.md.setSpeed(x)
            self.md.setTurningAngle(y)
            if x is 0 and y is 0:
                self.md.motorStop()

if __name__ == '__main__':
    subscribe()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
try:
    while True:
        print("Object "+str(uS.distanceForward())+"cm Forward")
        time.sleep(0.2)
        print("Object "+str(uS.distanceBackward())+"cm Backwards")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()