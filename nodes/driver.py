#!/usr/bin/env python3

# import imp
from curses import raw
from multiprocessing.spawn import import_main_path
from shutil import move
import rospy
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray, Float64
from firmware.MotorDriver import MotorDriver
import json

class subscribe:

    def __init__(self):
        rospy.init_node('motor_driver_node', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", String, self.callback)
        self.md = MotorDriver()


    def callback(self, data):
        print("The config is", data.data)
    
        self.parse(json.loads(data.data))
    
    def parse(self, raw_data):
        x = raw_data['x']
        y = raw_data['y']
        return 0



if __name__ == '__main__':
    subscribe()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")

