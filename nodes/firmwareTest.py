#!/usr/bin/env python

import imp
import json
import numpy as np
import rospy
import subprocess
import time
from std_msgs.msg import String

from BenchOS.firmware.CompassController.Compass import CompassData
from BenchOS.firmware.GPIO.GPIO_Controller import GPIO_Pins
from BenchOS.firmware.MotorControllers.Motors import Motors


class BigTest():
    def __init__(self):
        
#        cmd_vel_test = subprocess.Popen(["rosrun","robot-driver", "cmd_vel_test.py"])
        
        rospy.init_node('firmwareTest', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", String, self.callback)
        
        self.uS = GPIO_Pins()
        self.md = Motors()
        time.sleep(3)
        self.cD = CompassData()
        self.x = 0
        self.y = 0

    def callback(self, data):
        self.parse(json.loads(data.data))
    
    def parse(self, raw_data):
        
        self.x = raw_data['x']
        self.y = raw_data['y']
        
        print(str(self.x) + "|" +str(self.y))
        
        self.md.setMotors(self.x, self.y)
        
        if self.x is 0 and self.y is 0:
            self.md.stopMotors()
            
        if self.uS.distanceForward() < 10 and self.x > 0:
            self.md.stopMotors()
        elif self.uS.distanceBackward() < 10 and self.x < 0:
            self.md.stopMotors()
        self.md.write_read()
        
if __name__ == '__main__':
    bt = BigTest()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()    
