#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import String
import sys
import json
sys.path.append('..')
import firmware.MotorDriver


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
        if y is 0:
            self.md.decision('none')
        elif y < 0:
            self.md.decision('left')
        else:
            self.md.decision('right')
        self.md.setSpeed(x)
        self.md.move()
        if x is 0 and y is 0:
            self.md.motorStop()



if __name__ == '__main__':
    subscribe()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")

