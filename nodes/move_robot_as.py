#! /usr/bin/env python

import rospy
import actionlib
import parked_custom_msgs.msg
import time
from parked_custom_msgs.msg import Point
from parked_custom_msgs.msg import Robot_Sensor_State

class MoveRobot(object):

    # create messages that are used to publish feedback/result
    _feedback = parked_custom_msgs.msg.MoveToPointFeedback()
    _result = parked_custom_msgs.msg.MoveToPointResult()

    def __init__(self, name):
        self._current_pos = 0
        self._gps_pos = rospy.Subscriber('bench1/gps_pos', Point, self.update_current_pos)
        self._sensor_state = rospy.Subscriber('sensor_state', Robot_Sensor_State, self.update_sensor_state)
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, parked_custom_msgs.msg.MoveToPointAction, execute_cb=self.execute_cb, auto_start = False)
        print("server starting")
        self._as.start()

    def update_sensor_state(self, sensor_state):
        self._sensor_state = sensor_state

    def update_current_pos(self, point):
        self._current_pos = point
      
    def execute_cb(self, goal):
        # helper variables
        r = rospy.Rate(1)
        success = True
        print
        
        # get and set some initial values
        goal_pos = goal.destination
        self._feedback.intervention_required = False
        
        # appropriate conditions depend upon the obstacle avoidance algorithm, for example the robot is NEAR
        # the destination. (self._gps_pos is near goal_pos or self._sensor_state is clear or whatever).
        while True:
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break
            self._feedback.current_positon = self._current_pos
            # exact execution depends upon the algorithm
            if False:
                self._feedback.intervention_required = True
            # publish the feedback
            self._as.publish_feedback(self._feedback)
            # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
            r.sleep()
          
        if success:
            self._result.successful = True
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
        
if __name__ == '__main__':
    rospy.init_node('bench1_driver')
    server = MoveRobot(rospy.get_name())
    rospy.spin()