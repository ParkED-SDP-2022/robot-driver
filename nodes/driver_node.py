#!/usr/bin/env python

import imp
import json
import numpy as np
import rospy
import subprocess
import time
from geometry_msgs.msg import Twist

# from BenchOS.firmware.CompassController.Compass import CompassData
from BenchOS.firmware.GPIO.GPIO_Controller import GPIO_Pins
from BenchOS.firmware.MotorControllers.Motors import Motors


class BigTest():

    def __init__(self):
        
         # CONSTANTS
        self.LINEAR_FORWARDS_ENCODER_COUNT = 30
        self.LINEAR_BACKWARDS_ENCODER_COUNT = -30
        self.LINEAR_STATIONARY_ENCODER_COUNT = 0
        self.ANGULAR_RIGHT_ENCODER_COUNT = 20
        self.ANGULAR_LEFT_ENCODER_COUNT = -20
        self.ANGULAR_STATIONARY_ENCODER_COUNT = 0
        
        cmd_vel_test = subprocess.Popen(["rosrun","robot-driver", "cmd_vel_test1.py"])
        
        rospy.init_node('firmwareTest', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", Twist, self.callback)
        
        # self.uS = GPIO_Pins()
        self.md = Motors()
        time.sleep(3)
        # self.cD = CompassData()

        self.x = 0
        self.y = 0

    def callback(self, data):
        self.x = self.LINEAR_FORWARDS_ENCODER_COUNT if data.linear.x > 0 else \
            (self.LINEAR_BACKWARDS_ENCODER_COUNT if data.linear.x < 0 else self.LINEAR_STATIONARY_ENCODER_COUNT)
        self.y = self.ANGULAR_RIGHT_ENCODER_COUNT if data.angular.z > 0 else \
            (self.ANGULAR_LEFT_ENCODER_COUNT if data.angular.z < 0 else self.ANGULAR_STATIONARY_ENCODER_COUNT)
        
        print(str(self.x) + "|" +str(self.y))
        
        self.md.setMotors(self.x, self.y)
        
        if self.x is 0 and self.y is 0:
            self.md.stopMotors()
            
        # if self.uS.distanceForward() < 10 and self.x > 0:
        #     self.md.stopMotors()
        # elif self.uS.distanceBackward() < 10 and self.x < 0:
        #     self.md.stopMotors()

        self.md.write()
        
if __name__ == '__main__':
    bt = BigTest()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()    
