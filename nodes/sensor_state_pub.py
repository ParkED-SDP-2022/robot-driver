#!/usr/bin/env python

import imp
import rospy
import subprocess
import numpy as np
import json
import time

from parked_custom_msgs.msg import Robot_Sensor_State, Ultrasonic_Sensor, Compass
from geometry_msgs.msg import Twist

# OS libraries
from BenchOS.firmware.CompassController.Compass import CompassData
from BenchOS.firmware.UltrasonicControllers.Ultrasonic import UltrasonicSensor

class Sensor_State_Pub():
    def __init__(self):
        
#        cmd_vel_test = subprocess.Popen(["rosrun","robot-driver", "cmd_vel_test.py"])
        
        rospy.init_node('bench_x_sensor_state_pub', anonymous = True)
        self.publisher_name = rospy.Publisher('/bench_sensor_state', Robot_Sensor_State, queue_size=3)
        
        print('loading ultrasonic sensors')
        self.uS = UltrasonicSensor()
#         print('loading compass data')
#         self.cD = CompassData()
        print('everything up and running')
        
        self.sync()

    # Continuously reads and writes data to and from the robot.
    def sync(self):
        rate = rospy.Rate(40)
        while not rospy.is_shutdown():
            #print(self.cD.getHeading())
#             print(self.uS.distanceFLeft())
            # create the data packet for publishing as Robot_Sensor_State.
#             sensor_state = Robot_Sensor_State(Compass(self.cD.getHeading()), Ultrasonic_Sensor(self.uS.distanceFLeft()),
#                                               Ultrasonic_Sensor(self.uS.distanceFRight()),
#                                               Ultrasonic_Sensor(self.uS.distanceBackward()))
            sensor_state = Robot_Sensor_State(Compass(180), Ultrasonic_Sensor(250),
                                              Ultrasonic_Sensor(250),
                                              Ultrasonic_Sensor(250))
            print(sensor_state)
            self.publisher_name.publish(sensor_state)
            rate.sleep()
        
if __name__ == '__main__':
    bt = Sensor_State_Pub()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()    
