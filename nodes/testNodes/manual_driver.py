#!/usr/bin/env python
import imp
import rospy
import numpy as np
from std_msgs.msg import String
import json
from firmware.MotorDriver import *


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

