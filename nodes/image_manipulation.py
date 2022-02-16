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
    def imageSegmentation(self, image):
    
        #code here to produce 4 images from the camera feed
        
        roboCoords = self.distortionCorrection(images)
        return robotCoords
    def distortionCorrection(self, images):
        
        #code here to correct lens distortion in 4 images from the camera feed
        
        roboCoords = self.imageSplicing(images)
        return robotCoords
    
    def imageSplicing(self, images):
    
        #code here to splice images together from the camera feed
        
        roboCoords = self.colourSpaceCoordinate(image)
        return robotCoords
    
    def colourSpaceCoordinate(self, image):

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

