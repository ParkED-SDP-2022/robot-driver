#!/usr/bin/env python

import json
import random
import rospy
import sys
from std_msgs.msg import String


class Manual_testing:

    # Defines publisher and subscriber
    def __init__(self):

        # initialize the node named image_processing
        rospy.init_node('Manual_testing', anonymous=True)
        self.cmd_velPub = rospy.Publisher("/cmd_vel", String ,queue_size = 1)
        rate = rospy.Rate(500)  # 50hz
        # record the beginning time
        stime = rospy.get_time()
        while not rospy.is_shutdown():
            
            x = random.randrange(40,100)
            y = random.randrange(-40,40)
            y = 0
            cmd_vel = {'x': x, 'y': y}
            
            cmd_velData = json.dumps(cmd_vel)
            self.cmd_velPub.publish(cmd_velData)
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
