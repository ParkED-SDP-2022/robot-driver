#!/usr/bin/env python

from typing import Dict
import roslib
import sys
import rospy
import cv2
import numpy as np
import Process
import json
from Process import Image_processes
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Float64MultiArray, Float64, UInt8MultiArray
from cv_bridge import CvBridge, CvBridgeError

#----------------------------------------------------------------------------------------------------------

class Image_processes:

    def _init_(self):
        return       

    # Perform image processing
    def imProcess(self, image):

            red_u = (20,20,256)
            red_l = (0,0,100)
            climits = [[red_l,red_u]]
            
            masks = [cv2.inRange(image, climit[0], climit[1]) for climit in climits]
            maskJs = [cv2.cvtColor(mask,cv2.COLOR_BGR2RGB) for mask in masks]
          
            frames = [(image&maskJ) for maskJ in maskJs]
            
            gray_frames = [cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) for frame in frames]
            
            jThreshes = [cv2.threshold(gray_frame, 1, 255, cv2.THRESH_BINARY) for gray_frame in gray_frames]
            
            jcontours = [cv2.findContours(jthresh[1], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) for jthresh in jThreshes]
           
            cords = []
            radiuslist = []
            for jcontour in jcontours:
                # print(jcontour)
                try:    
                    Gradius = 0
                    (Gx,Gy),Gradius = cv2.minEnclosingCircle(self.mergeContors(jcontour[0]))
                    radiuslist.append(Gradius)
                    # print(Gradius)
                    if Gradius < 2: #Filter out single pixel showing
                        cords.append([-1,-1])
                    else:
                        cords.append([Gx,Gy])
                                
                except:
                    cords.append([-1,-1])
                    radiuslist.append(0)

            contourDic = {"Red": {'x':cords[3][0],'y':cords[3][1]}}
            
            im_copy = image.copy()
            
            for i in range(len(cords)):
                    cv2.circle(im_copy, (int(cords[i][0]), int(cords[i][1])), 2, (255, 255, 255), -1)
                    cv2.putText(im_copy, list(contourDic.keys())[i], (int(cords[i][0]) - 50, int(cords[i][1]) - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.circle(im_copy,(int(cords[i][0]), int(cords[i][1])),int(radiuslist[i]),(0,255,0),1)
                   
            return contourDic, im_copy
        
    def mergeContors(self, ctrs):
            list_of_pts = []
            for c in ctrs:
                    for e in c:
                            list_of_pts.append(e)
            ctr = np.array(list_of_pts).reshape((-1,1,2)).astype(np.int32)
            ctr = cv2.convexHull(ctr)
            return ctr


class image_converter:

  # Defines publisher and subscriber
  def __init__(self):
      
    self.yzCentres = None
    self.cv_image1 = None
    # initialize the node named image_processing
    rospy.init_node('camera_processor', anonymous=True)
    # initialize a publisher to send xz coordinates
    self.pos_pub = rospy.Publisher("robot_position", String ,queue_size = 1)
    # initialize a subscriber to recieve messages rom a topic named /robot/camera1/image_raw and use callback function to recieve data
    self.image_sub = rospy.Subscriber("/camera1/robot/image_raw",Image,self.callback1)
    # initialize the bridge between openCV and ROS
    self.bridge = CvBridge()
    rate = rospy.Rate(50)  # 5hz
    # record the beginning time
    while not rospy.is_shutdown():
        #print("Sending")
        self.showimg()
        rate.sleep()

  def showimg(self):
          # yzCentres = imageprocessor1.Contours(yzcontours)
    if self.yzCentres is None or self.cv_image1 is None:
      return
   
    cv2.imshow("Image 1",self.cv_image1)
    cv2.waitKey(1)
    
  # Recieve data from camera 1, process it, and publish
  def callback1(self,data):
    # Recieve the image
    try:
      imageprocessor1 = Image_processes()
      cv_image1_ps = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    # Publish the results
    try: 
      robotPositon,self.cv_image1 = imageprocessor1.imProcess(cv_image1_ps)
      
      self.pos_pub.publish(json.dumps({'bench1': robotPosition}))
      
    except CvBridgeError as e:
      print(e)

# call the class
def main(args):
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

# run the code if the node is called
if __name__ == '__main__':
    main(sys.argv)