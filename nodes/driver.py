#!/usr/bin/env python3

# import imp
from shutil import move
import rospy
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray, Float64
# from encoder_test_python import MotorDriver

class subscribe:

    def __init__(self):
        rospy.init_node('motor_driver_node', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/motor_driver_config", Float64, self.callback)


    def callback(self, data):
        print("The config is", data.data)
        move(data.data)
    
    def move(self, data):
        return 0



if __name__ == '__main__':
    subscribe()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")

