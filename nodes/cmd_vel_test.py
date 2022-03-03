#!/usr/bin/env python

import json
import random
import rospy
import sys
from std_msgs.msg import Twist

class Manual_testing:

    # Defines publisher and subscriber
    def __init__(self):

        # initialize the node named image_processing
        rospy.init_node('Manual_testing', anonymous=True)
        self.cmd_velPub = rospy.Publisher("/cmd_vel", Twist ,queue_size = 1)
        print("Robot Control")
        print("     w     ")
        print("a    s    d")
        print("     x     ")
        print("s to stop\n")
        rate = rospy.Rate(50)  # 5hz
        self.x = 0
        self.y = 0
        # record the beginning time
        stime = rospy.get_time()
        
        while not rospy.is_shutdown():
            key = raw_input("|Speed = "+ str(self.x) + " & Angular = " + str(self.y) + "|\n")
            if key is "x":
                self.x += -10
            if key is "s":
                self.x = 0
                self.y = 0
            if key is "w":
                self.x += 10
            if key is "d":
                self.y += 10
            if key is "a":
                self.y += -10
            self.y = self.y % 255
            self.x = self.x % 255
            cmd_vel = Twist()
            cmd_vel.linear.x = self.x
            cmd_vel.angular.x = self.y

            self.cmd_velPub.publish(cmd_vel)
            rate.sleep()

# --------------------------------------------------------------------------------------------------------------
def main(args):
    test = Manual_testing()

    try: 
        rospy.spin()

    except KeyboardInterrupt:
        print("Shutting down")


# run the code if the node is called
if __name__ == '__main__':
    main(sys.argv)
