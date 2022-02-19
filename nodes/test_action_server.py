#! /usr/bin/env python

import rospy
import actionlib
import parked_custom_msgs.msg
import time
from parked_custom_msgs.msg import Point

class MoveRobot(object):

    # create messages that are used to publish feedback/result
    _feedback = parked_custom_msgs.msg.Move_ForwardFeedback()
    _result = parked_custom_msgs.msg.Move_ForwardResult()

    def __init__(self, name):
        self._current_pos = 0
        self._gps_pos = rospy.Subscriber('bench1/gps_pos', Point, self.update_current_pos)
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, parked_custom_msgs.msg.Move_ForwardAction, execute_cb=self.execute_cb, auto_start = False)
        print("server starting")
        self._as.start()

    def update_current_pos(self, point):
        self._current_pos = point
      
    def execute_cb(self, goal):
        # helper variables
        r = rospy.Rate(1)
        success = True
        print
        
        # append the seeds for the fibonacci sequence
        goal_pos = goal.desired_goal
        self._feedback.time_left =  goal_pos.lat - time.perf_counter()
        
        # # publish info to the console for the user
        # rospy.loginfo('%s: Executing, creating fibonacci sequence of order %i with seeds %i, %i' % (self._action_name, goal.order, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        while self._current_pos.long < goal.desired_goal.long and self._current_pos.lat < goal.desired_goal.lat:
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break
            self._feedback.time_left = goal_pos.lat - time.perf_counter()
            print(self._feedback.time_left)
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