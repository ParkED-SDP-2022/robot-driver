#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import String
import json


class pathfinder:

    def __init__(self):
        rospy.init_node('pathfinder', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/bench_commands", String, self.callback)


    def callback(self, data):
        print("The config is", data.data)
    
        # this is how you parse the data
        parsed_data = json.loads(data.data)
    



if __name__ == '__main__':
    pathfinder()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")

