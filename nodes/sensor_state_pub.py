#! /usr/bin/env python

# some random stackoverflow stuff to make it possible to import packages.
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())

sys.path.append(a)

import rospy
from parked_custom_msgs.msg import Robot_Sensor_State

# firmware files uncomment when testing on PI!!!!
# from BenchOS.firmware.CompassController import Compass
# from BenchOS.firmware.UltrasonicControllers import Ultrasonic

class Sensor_State_Pub:

    def __init__(self):
        rospy.init_node('sensor_state_pub', anonymous=False)
        self.sensor_state_pub = rospy.Publisher('sensor_state', Robot_Sensor_State, queue_size=10)
        self.sensor_state_data = Robot_Sensor_State()
        # uncomment when testing on PI!!!!
        # self.compass_controller = Compass.CompassData()
        # self.ultrasonic_controller = Ultrasonic.UltrasonicSensor()
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():

            # call appropriate methods from imported firmware files, populate sensor_state_data!!!!!
            # after this the node will be fully operational

            self.sensor_state_pub.publish(self.sensor_state_data)

            rate.sleep()
    


def main(args):
    pub = Sensor_State_Pub()
    try: 
            rospy.spin()

    except KeyboardInterrupt:
        print("Shutting down")


# run the code if the node is called
if __name__ == '__main__':
    main(sys.argv)
