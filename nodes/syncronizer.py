#!/usr/bin/env python

import time

import rospy
from geometry_msgs.msg import Twist

# OS libraries
from BenchOS.firmware.MotorControllers.Motors import Motors


class Syncronizer():
    def __init__(self):

#        cmd_vel_test = subprocess.Popen(["rosrun","robot-driver", "cmd_vel_test.py"])

        rospy.init_node('bench_x_yncronizer', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", Twist, self.callback)

        self.input_from_serial = []

        #self.uS = UltrasonicSensor()
        self.md = Motors()
        time.sleep(3)
        #self.cD = CompassData()
        self.x = None
        self.y = 0
        self.zeroed = 0
        self.prev_x = 0
        self.prev_y = 0
        self.rate = rospy.Rate(4)
        self.accel_in_progress = False
        self.sync()

    # Continuously reads and writes data to and from the robot.
    def sync(self):

        while not rospy.is_shutdown():
            try:
                self.input_from_serial = self.md.write_read()
            except:
                print("failed read, continuing")
            self.rate.sleep()

    def runsmooth(self, x):

        speed = 110

        #forward
        if x == 1:
            while True:
                time.sleep(0.25)
                self.md.setMotors(speed, 0)
                lastl_fwd = self.input_from_serial[4]
                lastr_fwd = self.input_from_serial[6]
                time.sleep(0.25)

                if lastl_fwd+10 >= self.input_from_serial[4] and lastr_fwd+10 >= self.input_from_serial[6]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(80, 0)
                    break
        #backward
        elif x == 2:
            while True:
                time.sleep(0.25)
                self.md.setMotors(-speed, 0)
                lastl_bwd = self.input_from_serial[4]
                lastr_bwd = self.input_from_serial[6]
                time.sleep(0.25)

                if lastl_bwd-10 >= self.input_from_serial[4] and lastr_bwd-10 <= self.input_from_serial[6]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(-80, 0)
                    break
        #stop left
        elif x == 3:
            while True:
                time.sleep(0.25)
                self.md.setMotors(0, -speed)
                lastl_bwd = self.input_from_serial[4]
                lastr_fwd = self.input_from_serial[6]
                time.sleep(0.25)

                if lastl_bwd - 10 <= self.input_from_serial[4] and lastr_fwd + 10 >= self.input_from_serial[6]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(0, -80)
                    break
        #stop right
        elif x == 4:
            while True:
                time.sleep(0.25)
                self.md.setMotors(0, speed)
                lastl_fwd = self.input_from_serial[4]
                lastr_bwd = self.input_from_serial[6]
                time.sleep(0.25)

                if lastl_fwd + 10 >= self.input_from_serial[4] and lastr_bwd - 10 <= self.input_from_serial[6]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(0, 80)
                    break

    def callback(self, data):
        self.parse(data)

    def parse(self, raw_data):

        self.x = raw_data.linear.x # 0 | 1
        self.y = raw_data.angular.z # 0 | 1

        print("cmd x = "+str(self.x) + " | cmd y = " + str(self.y))

        #check for any changes otherwise do nothing
        if self.prev_x != self.x and self.prev_y != self.y:
            if self.x == 1: #and self.y == 0:
                self.runsmooth(1)

            if self.x == -1: #and self.y == 0:
                self.runsmooth(2)

            if self.x == 1 and self.y == 1:
                self.runsmooth(1)

            if self.x == -1 and self.y == 1:
                self.runsmooth(2)

            if self.x == 1 and self.y == -1:
                self.runsmooth(1)

            if self.x == -1 and self.y == -1:
                self.runsmooth(2)

            if self.x == 0 and self.y == 0:
                self.md.setMotors(0,0)

            if self.x == 0 and self.y == -1:
                self.runsmooth(3)

            if self.x == 0 and self.y == 1:
                self.runsmooth(4)

if __name__ == '__main__':
    bt = Syncronizer()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()
