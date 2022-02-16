#!/usr/bin/env python3

import json
from typing import Dict
import random
from numpy.lib.function_base import angle
import roslib
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Float64MultiArray, Float64


class Manual_testing:

    # Defines publisher and subscriber
    def __init__(self):

        # initialize the node named image_processing
        rospy.init_node('Manual_testing', anonymous=True)
        self.cmd_velPub = rospy.Publisher("/cmd_vel", String ,queue_size = 1)
        rate = rospy.Rate(50)  # 5hz
        # record the beginning time
        stime = rospy.get_time()
        while not rospy.is_shutdown():
            
            x = random.randrange(10,20)
            y = random.randrange(0,1)
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
    cv2.destroyAllWindows()


# run the code if the node is called
if __name__ == '__main__':
    main(sys.argv)
