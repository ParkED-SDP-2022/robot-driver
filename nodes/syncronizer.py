#!/usr/bin/env python

import imp
import rospy
import subprocess
import numpy as np
from std_msgs.msg import String
import json
import time

from geometry_msgs.msg import Twist

# OS libraries
from BenchOS.firmware.CompassController.Compass import CompassData
from BenchOS.firmware.MotorControllers.Motors import Motors
from BenchOS.firmware.UltrasonicControllers.Ultrasonic import UltrasonicSensor

class Syncronizer():
    def __init__(self):

#        cmd_vel_test = subprocess.Popen(["rosrun","robot-driver", "cmd_vel_test.py"])

        rospy.init_node('bench_x_yncronizer', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", Twist, self.callback)

        self.input_from_serial = []

        self.uS = UltrasonicSensor()
        self.md = Motors()
        time.sleep(3)
        self.cD = CompassData()
        self.x = 0
        self.y = 0
        self.zeroed = 0
        self.rate = rospy.Rate(4)
        self.sync()

    # Continuously reads and writes data to and from the robot.
    def sync(self):

        while not rospy.is_shutdown():
            try:
                self.input_from_serial = self.md.write_read()
            except:
                print("failed read, continuing")
            self.rate.sleep()

    def runsmooth(self, x):
        return x
    def callback(self, data):
        self.parse(data)

    def parse(self, raw_data):

        self.x = raw_data.linear.x # 0 | 1
        self.y = raw_data.angular.z # -20 -> 20

        print(str(self.x) + "|" + str(self.y))

        if self.x == 1: #and self.y == 0:
            #self.runsmooth(1)
             self.md.setMotors(110, self.y)
#              self.input_from_serial = self.md.write_read()
             self.rate.sleep()
             self.md.setMotors(80, self.y)
#              self.input_from_serial = self.md.write_read()
             self.rate.sleep()

        if self.x == -1: #and self.y == 0:
            #self.runsmooth(2)
             self.md.setMotors(-110, self.y)
#              self.input_from_serial = self.md.write_read()
             self.rate.sleep()
             self.md.setMotors(-80, self.y)
#              self.input_from_serial = self.md.write_read()
             self.rate.sleep()

        #if self.x == 1 and self.y == 1:
            #self.runsmooth(3)

        #if self.x == -1 and self.y == 1:
            #self.runsmooth(4)

        #if self.x == 1 and self.y == -1:
            #self.runsmooth(5)

        #if self.x == -1 and self.y == -1:
            #self.runsmooth(6)

        if self.x == 0: #and self.y == 0:
            self.md.setMotors(0,0)

        #if self.x == 0 and self.y == -1:
            #self.runsmooth(7)

        #if self.x == 0 and self.y == -1:
            #self.runsmooth(8)

if __name__ == '__main__':
    bt = Syncronizer()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()
