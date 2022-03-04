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
        

        self.uS = UltrasonicSensor()
        print('1')
        time.sleep(3)
        self.cD = CompassData()
        print('2')
        
        self.sync()

    # Continuously reads and writes data to and from the robot.
    def sync(self):
        rate = rospy.Rate(40)
        while not rospy.is_shutdown():
            print('3')
            # create the data packet for publishing as Robot_Sensor_State.
            sensor_state = Robot_Sensor_State(Compass(self.cD.getHeading()), Ultrasonic_Sensor(self.uS.distanceForward()),
                                              Ultrasonic_Sensor(self.uS.distanceBackward()))
            print('4')
            self.publisher_name.publish(sensor_state)
            print('5')
            rate.sleep()
        
if __name__ == '__main__':
    bt = Sensor_State_Pub()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()    
