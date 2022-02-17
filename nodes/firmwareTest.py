#!/usr/bin/env python
import imp
import rospy
import subprocess
import numpy as np
from std_msgs.msg import String
import json
import time
from BenchOS.firmware.CompassController.Compass import CompassData
from BenchOS.firmware.MotorControllers.MotorDriver import MotorDriver
from BenchOS.firmware.UltrasonicControllers.Ultrasonic import UltrasonicSensor

class BigTest():
    def __init__(self):
        
        self.uS = UltrasonicSensor()
        self.md = MotorDriver()
        self.cD = CompassData()
        self.x = 0
        self.y = 0

        motorListener = subprocess.Popen(["rosrun", "robot-driver", "cmd_vel_test.py"])
        
        rospy.init_node('firmwareTest', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", String, self.callback)
        
        while not rospy.is_shutdown():
#             print("Object "+str(self.uS.distanceForward())+"cm Forward")
#             time.sleep(0.2)
#             print("Object "+str(self.uS.distanceBackward())+"cm Backwards")
#             time.sleep(0.2)
            if self.uS.distanceForward() < 10 and self.x > 0:
                self.md.motorStop()
            elif self.uS.distanceBackward() < 10 and self.x < 0:
                self.md.motorStop()

    def callback(self, data):
        print("The config is", data.data)
        self.parse(json.loads(data.data))
    
    def parse(self, raw_data):
        
        self.x = raw_data['x']
        self.y = raw_data['y']
        
        self.md.setSpeed(self.x)
        self.md.setTurningAngle(self.y)
        if self.x is 0 and self.y is 0:
            self.md.motorStop()
        
        self.cD.getUpdate()

if __name__ == '__main__':
    bt = BigTest()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()    