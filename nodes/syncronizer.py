#!/usr/bin/env python

import time
import rospy
from simple_pid import PID
from geometry_msgs.msg import Twist

# OS libraries
from BenchOS.firmware.MotorControllers.Motors import Motors

class Q():

    def __init__(self):
        self.queue = [0,0,0,0]
        self.queueHead = 0
        self.queueTail = 0

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

        rospy.init_node('bench_x_yncronizer', anonymous = True)
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

        self.lastl_fwd = 0
        self.lastr_fwd = 0
        self.lastl_bwd = 0
        self.lastr_bwd = 0
        
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
        
        self.lastl_bwd = self.leftQueue.front()
        self.lastl_fwd = self.leftQueue.front()
        self.lastr_bwd = self.rightQueue.front()
        self.lastr_fwd = self.rightQueue.front()
        
    def runsmooth(self, x):

        speed = 120
        #forward
        if x == 1:
#             while True:
#             self.update()
            speed = 120
            self.md.setMotors(speed, 0)
            time.sleep(0.25)
            self.md.setMotors(0, 0)
            print("ramping up speed @ ", speed)
                
#                 if self.lastl_fwd >= self.status[4] or self.lastr_fwd >= self.status[5]:
#                     print("stall")
#                     speed += 10
#                 else:
#                     self.md.setMotors(self.cruise_speed, 0)
#                     break
        #backward
        elif x == 2:
#             while True:
            
#             self.update()
            speed = 120
            self.md.setMotors(-speed, 0)
            time.sleep(0.2)
            self.md.setMotors(0, 0)
            print("ramping up speed @ ", -speed)
# 
#                 if self.lastl_bwd <= self.status[4] or self.lastr_bwd <= self.status[5]:
#                     print("stall")
#                     speed += 10
#                 else:
#                     self.md.setMotors(-self.cruise_speed, 0)
#                     break
        #stop left
        elif x == 3:
#             while True:
#             self.update()
            speed = 130
            self.md.setMotors(0, -speed)
            time.sleep(0.2)
            self.md.setMotors(0, 0)
            print("ramping up turning @ ", -speed)
# 
#                 if self.lastl_bwd <= self.status[4] or self.lastr_fwd >= self.status[5]:
#                     print("stall")
#                     speed += 10
#                 else:
#                     self.md.setMotors(0, -self.static_turn)
#                     break
#                 
#                 if speed>130:
#                     break
        #stop right
        elif x == 4:
#             while True:
                
#             self.update()
            speed = 130
            self.md.setMotors(0, speed)
            time.sleep(0.2)
            self.md.setMotors(0, 0)
            print("ramping up turning @ ", speed)
#             time.sleep(0.25)
            

#                 if self.lastl_fwd >= self.status[4] or self.lastr_bwd<= self.status[5]:
#                     print("stall")
#                     speed += 10
#                 else:
#                     self.md.setMotors(0, self.static_turn)
#                     break
#                 if speed>130:
#                     break

    def clear(self):
        self.leftQueue.clear()
        self.rightQueue.clear()

    def callback(self, data):

        self.prev_x = self.x
        self.prev_y = self.y
        
        self.x = data.linear.x # 0 | 1
        self.y = data.angular.z # 0 | 1

        #print("cmd x = "+str(self.x) + " | cmd y = " + str(self.y))
        #print("prevx:"+str(self.prev_x)+" prevy"+str( self.prev_y))
        #check for any changes otherwise do nothing
        print("changed values")
        if self.x == 1 and self.y == 0:
            self.runsmooth(1)
            print("fwdscale")

        if self.x == -1 and self.y == 0:
            self.runsmooth(2)
            print("bwdscale")
#             
#         if self.prev_x != self.x:
#             print("x changed")
            
#             if self.x == 1 and self.y == 1:
#                 self.runsmooth(1)
#                 print("fwdR ")
#                 self.md.setMotors(self.cruise_speed, self.turn_speed)
# 
#             if self.x == -1 and self.y == 1:
#                 self.runsmooth(2)
#                 
#                 print("bwdR ")
#                 self.md.setMotors(-self.cruise_speed, self.turn_speed)
# 
#             if self.x == 1 and self.y == -1:
#                 self.runsmooth(1)
#                 
#                 print("fwdL ")
#                 self.md.setMotors(self.cruise_speed, -self.turn_speed)
# 
#             if self.x == -1 and self.y == -1:
#                 self.runsmooth(2)
#                 
#                 print("bwdL ")
#                 self.md.setMotors(-self.cruise_speed, -self.turn_speed)
#         else:
#             
#             print("no x change")
#             if self.x == 1 and self.y == 1:
#                 self.md.setMotors(self.cruise_speed, self.turn_speed)
#                 print("fwdR ")
# 
#             if self.x == -1 and self.y == 1:
#                 self.md.setMotors(-self.cruise_speed, self.turn_speed)
#                 print("bwdR ")
# 
#             if self.x == 1 and self.y == -1:
#                 self.md.setMotors(self.cruise_speed, -self.turn_speed)
#                 print("fwdL ")
# 
#             if self.x == -1 and self.y == -1:
#                 self.md.setMotors(-self.cruise_speed, -self.turn_speed)
#                 print("bwdL ")

        if self.x == 0 and self.y == 0:
            print("stopping")
            self.md.stopMotors()

        if self.x == 0 and self.y == -1:
            self.runsmooth(3)
#             print("static left")
#             self.md.setMotors(0, -self.static_turn)

        if self.x == 0 and self.y == 1:
            self.runsmooth(4)
#             print("static right")
#             self.md.setMotors(0, self.static_turn)

        self.clear()

        # check for movement and if none, adjust cruise / turn speeds
#         else:
#             
#             if self.x == 0 and self.y == 0:
#                 print("stopping")
#                 self.md.stopMotors()
# 
# 
#             #check to see it moves forward geting the general encoder difference and increase speed if not moving
#             if self.x == 1 and self.y == 0 and (self.rightQueue.getDiff() == 0 or self.leftQueue.getDiff() == 0):
#                 self.cruise_speed += 1
#                 print("cruise speed is not effective")
#                 print("new speed = ", self.cruise_speed)
#                 self.md.setMotors(self.cruise_speed,0)
# 
# 
#             # check to see it moves backward geting the general encoder difference and increase speed if not moving
#             if self.x == -1 and self.y == 0 and (self.rightQueue.getDiff() == 0 or self.leftQueue.getDiff() == 0):
#                 self.cruise_speed += 1
#                 print("cruise speed is not effective backwards")
#                 print("new speed = ", -self.cruise_speed)
#                 self.md.setMotors(-self.cruise_speed,0)
# 
# 
#             if self.x == 1 and self.y == 1 and not (self.rightQueue.getAve() > self.leftQueue.getAve()):
#                 self.turn_speed += 1
#                 print("turn speed is not effective forward right")
#                 print("new turn speed = ", self.turn_speed)
#                 self.md.setMotors(self.cruise_speed, self.turn_speed)
# 
# 
#             if self.x == -1 and self.y == 1 and not (self.rightQueue.getAve() > self.leftQueue.getAve()):
#                 self.turn_speed += 1
#                 print("turn speed is not effective backward right")
#                 print("new turn speed = ", self.turn_speed)
#                 self.md.setMotors(-self.cruise_speed, self.turn_speed)
# 
# 
#             if self.x == 1 and self.y == -1 and not (self.rightQueue.getAve() < self.leftQueue.getAve()):
#                 self.turn_speed += 1
#                 print("turn speed is not effective forward left")
#                 self.md.setMotors(self.cruise_speed, -self.turn_speed)
# 
# 
#             if self.x == -1 and self.y == -1 and not (self.rightQueue.getAve() < self.leftQueue.getAve()):
#                 self.turn_speed += 1
#                 print("turn speed is not effective backward left")
#                 print("new turn speed = ", -self.turn_speed)
#                 self.md.setMotors(-self.cruise_speed, -self.turn_speed)
# 
# 
#             if self.x == 0 and self.y == -1 and not (self.rightQueue.getAve() > self.leftQueue.getAve()):
#                 self.static_turn += 1
#                 print("static speed is not effective left")
#                 print("new static speed = ", -self.turn_speed)
#                 self.md.setMotors(0, -self.turn_speed)
# 
# 
#             if self.x == 0 and self.y == 1 and not (self.rightQueue.getAve() < self.leftQueue.getAve()):
#                 self.static_turn += 1
#                 print("static speed is not effective right")
#                 print("new static speed = ", self.turn_speed)
#                 self.md.setMotors(0, self.turn_speed)
        

if __name__ == '__main__':
    bt = Syncronizer()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        GPIO.cleanup()
