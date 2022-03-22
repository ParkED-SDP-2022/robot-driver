#!/usr/bin/env python

import rospy
import time
from geometry_msgs.msg import Twist
from simple_pid import PID

# OS libraries
from BenchOS.firmware.MotorControllers.Motors import Motors


class Q():

    def __init__(self):
        self.queue = [0,0,0,0]
        self.queueHead = 0
        self.queueTail = 1

    def clear(self):
        for i in range(0, len(self.queue)-1, 1):
            self.queue[i] = 0

    def enqueue(self, value):
        self.queue[self.queueHead] = value
        self.queueHead += 1
        if self.queueHead > len(self.queue)-1:
            self.queueHead = 0
        if self.queueTail == self.queueHead:
            self.queueHead +=1
        if self.queueTail > len(self.queue)-1:
            self.queueTail = 0

    def getAve(self):
        sum = 0
        for i in range(0, len(self.queue)-1, 1):
            if self.queue[i] != 0:
                sum += self.queue[i]
        return sum / len(self.queue)

    def getDiff(self):
        return max(self.queue) - self.getAve()

    def front(self):
        return self.queue[self.queueHead]

class Syncronizer():
    def __init__(self):
        rospy.init_node('bench_x_yncronizer', anonymous=True)
        self.subscriber_name = rospy.Subscriber("/cmd_vel", Twist, self.callback)

        self.status = []
        self.md = Motors()
        time.sleep(2)
        self.x = 0
        self.y = 0
        self.prev_x = 0
        self.prev_y = 0
        self.rate = rospy.Rate(4)
        self.cruise_speed = 60
        self.turn_speed = 20
        self.static_turn = 80
        self.rightQueue = Q()
        self.leftQueue = Q()
        self.lastl_bwd = 0
        self.lastr_bwd = 0


        self.leftPID = PID(1, 0.1, 0.05, setpoint=0)
        self.rightPID = PID(1, 0.1, 0.05, setpoint=0)
        self.rightPID.output_limits(-255,255)
        self.leftPID.output_limits(-255,255)

        print("Ready for commands")
        self.sync()

    # Continuously reads and writes data to and from the robot.
    def sync(self):

        while not rospy.is_shutdown():
            try:
                self.status = self.md.write_read()
            
            except:
                print("bad read, continuing")
            
            self.leftQueue.enqueue(self.status[4])
            self.rightQueue.enqueue(self.status[5])
            self.rate.sleep()
            
    def update(self):
        
        self.left = self.leftQueue.front()
        self.right = self.rightQueue.front()

    def clear(self):
        self.leftQueue.clear()
        self.rightQueue.clear()

    def callback(self, data):

        self.prev_x = self.x
        self.prev_y = self.y
        
        self.x = data.linear.x # 0 | 1
        self.y = data.angular.z # 0 | 1

        self.rightPID.setpoint = data.linear.x
        self.leftPID.setpoint = data.angular.z



if __name__ == '__main__':
    bt = Syncronizer()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()
