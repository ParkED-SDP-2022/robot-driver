#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import Twist

# OS libraries
from BenchOS.firmware.MotorControllers.Motors import Motors

class Q():

    def __init__(self):
        self.queue = [0,0,0,0]
        self.queueHead = 0
        self.queueTail = 1

    def clear(self):
        for i in range(0, len(self.queue), 1):
            self.queue[i] = 0

    def enqueue(self, value):
        self.queue[self.queueHead] = 0
        self.queueHead += 1
        if self.queueHead > len(self.queue):
            self.queueHead = 0
        if self.queueTail == self.queueHead:
            self.queueTail +=1
        if self.queueTail > len(self.queue):
            self.queueTail = 0

    def getAve(self):
        for i in range(0, len(self.queue), 1):
            if self.queue[i] != 0:
                sum += self.queue[i]
        return sum / len(self.queue)

    def getDiff(self):
        return max(self.queue) - self.getAve()


class Syncronizer():
    def __init__(self):

        rospy.init_node('bench_x_yncronizer', anonymous = True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", Twist, self.callback)

        self.input_from_serial = []
        self.md = Motors()
        time.sleep(3)
        self.x = 0
        self.y = 0
        self.prev_x = 0
        self.prev_y = 0
        self.rate = rospy.Rate(4)
        self.cruise_speed = 70
        self.turn_speed = 20
        self.static_turn = 80
        self.rightQueue = Q()
        self.leftQueue = Q()

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
                lastl_fwd = self.input_from_serial[3]
                lastr_fwd = self.input_from_serial[5]
                time.sleep(0.25)

                if lastl_fwd+10 >= self.input_from_serial[3] and lastr_fwd+10 >= self.input_from_serial[5]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(self.cruise_speed, 0)
                    break
        #backward
        elif x == 2:
            while True:
                time.sleep(0.25)
                self.md.setMotors(-speed, 0)
                lastl_bwd = self.input_from_serial[4]
                lastr_bwd = self.input_from_serial[6]
                time.sleep(0.25)

                if lastl_bwd-10 >= self.input_from_serial[3] and lastr_bwd-10 <= self.input_from_serial[5]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(-self.cruise_speed, 0)
                    break
        #stop left
        elif x == 3:
            while True:
                time.sleep(0.25)
                self.md.setMotors(0, -speed)
                lastl_bwd = self.input_from_serial[4]
                lastr_fwd = self.input_from_serial[6]
                time.sleep(0.25)

                if lastl_bwd - 10 <= self.input_from_serial[3] and lastr_fwd + 10 >= self.input_from_serial[5]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(0, -self.static_turn)
                    break
        #stop right
        elif x == 4:
            while True:
                time.sleep(0.25)
                self.md.setMotors(0, speed)
                lastl_fwd = self.input_from_serial[4]
                lastr_bwd = self.input_from_serial[6]
                time.sleep(0.25)

                if lastl_fwd + 10 >= self.input_from_serial[3] and lastr_bwd - 10 <= self.input_from_serial[5]:
                    self.md.stopMotors()
                    speed += 10
                else:
                    self.md.setMotors(0, self.static_turn)
                    break

    def clear(self):
        self.leftQueue.clear()
        self.rightQueue.clear()

    def callback(self, data):
        self.parse(data)

    def parse(self, raw_data):

        self.x = raw_data.linear.x # 0 | 1
        self.y = raw_data.angular.z # 0 | 1

        print("cmd x = "+str(self.x) + " | cmd y = " + str(self.y))

        #check for any changes otherwise do nothing
        if self.prev_x != self.x and self.prev_y != self.y:
            if self.x == 1 and self.y == 0:
                self.runsmooth(1)

            if self.x == -1 and self.y == 0:
                self.runsmooth(2)
            if self.prev_x != self.x:
                if self.x == 1 and self.y == 1:
                    self.runsmooth(1)
                    self.md.setMotors(self.cruise_speed, self.turn_speed)

                if self.x == -1 and self.y == 1:
                    self.runsmooth(2)
                    self.md.setMotors(-self.cruise_speed, self.turn_speed)

                if self.x == 1 and self.y == -1:
                    self.runsmooth(1)
                    self.md.setMotors(self.cruise_speed, -self.turn_speed)

                if self.x == -1 and self.y == -1:
                    self.runsmooth(2)
                    self.md.setMotors(-self.cruise_speed, -self.turn_speed)
            else:
                if self.x == 1 and self.y == 1:
                    self.md.setMotors(self.cruise_speed, self.turn_speed)

                if self.x == -1 and self.y == 1:
                    self.md.setMotors(-self.cruise_speed, self.turn_speed)

                if self.x == 1 and self.y == -1:
                    self.md.setMotors(self.cruise_speed, -self.turn_speed)

                if self.x == -1 and self.y == -1:
                    self.md.setMotors(-self.cruise_speed, -self.turn_speed)

            if self.x == 0 and self.y == 0:
                self.md.setMotors(0,0)

            if self.x == 0 and self.y == -1:
                self.runsmooth(3)
                self.md.setMotors(0, -self.static_turn)

            if self.x == 0 and self.y == 1:
                self.runsmooth(4)
                self.md.setMotors(0, -self.static_turn)

            self.clear()

        # check for movement and if none, adjust cruise / turn speeds
        else:
            self.leftQueue.enqueue(self.input_from_serial[3])
            self.rightQueue.enqueue(self.input_from_serial[5])

            #check to see it moves forward geting the general encoder difference and increase speed if not moving
            if self.x == 1 and self.y == 0 and (self.rightQueue.getDiff() == 0 or self.leftQueue.getDiff() == 0):
                self.cruise_speed += 1
                self.md.setMotors(self.cruise_speed)

            # check to see it moves backward geting the general encoder difference and increase speed if not moving
            if self.x == -1 and self.y == 0 and (self.rightQueue.getDiff() == 0 or self.leftQueue.getDiff() == 0):
                self.cruise_speed += 1
                self.md.setMotors(-self.cruise_speed)

            if self.x == 1 and self.y == 1 and not (self.rightQueue.getAve() > self.leftQueue.getAve()):
                self.turn_speed += 1
                self.md.setMotors(self.cruise_speed, self.turn_speed)

            if self.x == -1 and self.y == 1 and not (self.rightQueue.getAve() > self.leftQueue.getAve()):
                self.turn_speed += 1
                self.md.setMotors(-self.cruise_speed, self.turn_speed)

            if self.x == 1 and self.y == -1 and not (self.rightQueue.getAve() < self.leftQueue.getAve()):
                self.turn_speed += 1
                self.md.setMotors(self.cruise_speed, -self.turn_speed)

            if self.x == -1 and self.y == -1 and not (self.rightQueue.getAve() < self.leftQueue.getAve()):
                self.turn_speed += 1
                self.md.setMotors(-self.cruise_speed, -self.turn_speed)

            if self.x == 0 and self.y == -1 and not (self.rightQueue.getAve() > self.leftQueue.getAve()):
                self.static_turn += 1
                self.md.setMotors(0, -self.turn_speed)

            if self.x == 0 and self.y == 1 and not (self.rightQueue.getAve() < self.leftQueue.getAve()):
                self.static_turn += 1
                self.md.setMotors(0, self.turn_speed)


if __name__ == '__main__':
    bt = Syncronizer()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()
