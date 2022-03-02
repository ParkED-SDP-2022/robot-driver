#!/usr/bin/python

import os
import time

import cv2
import numpy as np

import smbus
from picamera import PiCamera
from picamera.array import PiRGBArray


class Camera:
    __camera_resolution = {'low':    (160, 128),
                           'medium': (640, 480),
                           'high':   (800, 608)}

    def __init__(self, onRobot):
        self.__onRobot = onRobot
        self.__openCam = False

    def initCamera(self, camera='pi', resolution='low'):
        """
        Keyword arguments:
            camera -- which camera hardware to use:
                pi, logitech (default 'pi')

            resolution -- the camera resolution to use:
                low, medium, high (default 'low')
        """
        if resolution not in Camera.__camera_resolution:
            print('[ERROR] Camera.__init__(): Unknown \'{}\' camera resolution.'.format(resolution))
            return

        if camera == 'pi':
            self.__camera = PiCamera(resolution=Camera.__camera_resolution[resolution])
            self.__rawCapture = PiRGBArray(self.__camera, size=Camera.__camera_resolution[resolution])
            time.sleep(0.2)
            self.getFrame = self.__getFramePi
        elif camera == 'logitech':
            self.__openLogitech()
            self.__setLogitechResolution(resolution)
            self.getFrame = self.__getFrameLogitech
        else:
            print('[ERROR] Camera.__init__(): Unknown \'{}\' camera.'.format(camera))

        return self

    def imshow(self, wnd, img):
        if not self.__onRobot:
            if img.__class__ != np.ndarray:
                print('[ERROR] Camera.imshow(): Invalid image.')
                return False
            else:
                cv2.imshow(wnd, img)
                cv2.waitKey(1) & 0xFF

    def destroy(self):
        if self.__openCam:
            self.__cap.release()
        self.__openCam = False

    def __getFramePi(self):
        self.__camera.capture(self.__rawCapture, format='bgr', use_video_port=True)
        frame = self.__rawCapture.array
        self.__rawCapture.truncate(0)
        return frame

    def __getFrameLogitech(self):
        self.__cap.grab()
        (_, img) = self.__cap.retrieve()
        return img

    def __openLogitech(self):
        if not os.path.exists('/dev/video0'):
            return False
        self.__cap = cv2.VideoCapture()
        if not self.__cap.open(-1):
            return False
        self.__openCam = True

    def __setLogitechResolution(self, resolution):
        while not self.__openCam:
            print('Setting camera resolution to {} - {}'.format(resolution, self.__openCam))
            time.sleep(0.2)
        if self.__openCam:
            self.__cap.set(3, Camera.__camera_resolution[resolution][0])
            self.__cap.set(4, Camera.__camera_resolution[resolution][1])


class IOTools:
    __version = '2018a'

    def __init__(self, onRobot):
        print('[IOTools] R:SS IOTools ' + IOTools.__version)
        self.camera = Camera(onRobot)

    def destroy(self):
        self.camera.destroy()
        self.motor_control.stopMotors()
