#!/usr/bin/env python

import json
import random
import rospy
import sys
from std_msgs.msg import String


class PublisherForPathfidning:

    # Defines publisher and subscriber
    def __init__(self):

        # initialize the node named image_processing
        rospy.init_node('Publisher_for_Pathfinder', anonymous=True)
        self.bench_commands = rospy.Publisher("/bench_commands", String ,queue_size = 1)
        rate = rospy.Rate(500)  # 50hz
        # record the beginning time
        stime = rospy.get_time()
        while not rospy.is_shutdown():
         
            bench_commands = {
                'bench1': {
                    'long': -2.34556454,
                    'lat': -4.45656456
                },
                'bench2': {
                    'long': 2.34556454,
                    'lat': -6.45656456
                },
                'bench3': {
                    'long': -2.34556454,
                    'lat': -9.45656456
                }
            }
            
            bench_commands_data = json.dumps(bench_commands)
            self.bench_commands.publish(bench_commands_data)
            rate.sleep()

# --------------------------------------------------------------------------------------------------------------
def main(args):
    test = PublisherForPathfidning()

    try: 
        rospy.spin()

    except KeyboardInterrupt:
        print("Shutting down")


# run the code if the node is called
if __name__ == '__main__':
    main(sys.argv)
