#!/usr/bin/python

import os
import time
import cv2
import numpy as np
from smbus2 import SMBus
from time import sleep
from datetime import datetime

class Motors(object):
    def __init__(self):
        
        print "Starting SMBus . . ."
        self.bus = SMBus(1)
        sleep(0.2)
        print "SMBus Started."
        self.tRexSlaveAddress = 0x07
        self.num_encoder_ports = 24 #d5 & d6 for motors
        
        #command packet values
        self.sb = 0x0f #start Byte
        self.pwm = 0x06 #motor pwm frequency 0-7
        self.lmH = 0x00 #left motor speed word || -255 to max 255
        self.lmL = 0xff #left motor speed word || -255 to max 255
        self.lmB = 0x00 #left motor break || 0 or 1
        self.rmH = 0x00 #right motor speed word || max 255
        self.rmL = 0xff #right motor speed word || max 255
        self.rmB = 0x00 #right motor break || 0 or 1
        self.servo0H = 0x00 #servo 0 word
        self.servo0L = 0x00 #servo 0 word
        self.servo1H = 0x00 #servo 1 word
        self.servo1L = 0x00 #servo 1 word
        self.servo2H = 0x00 #servo 2 word
        self.servo2L = 0x00 #servo 2 word
        self.servo3H = 0x00 #servo 3 word
        self.servo3L = 0x00 #servo 3 word
        self.servo4H = 0x00 #servo 4 word || must be set to 0 to disable servo pulses
        self.servo4L = 0x00 #servo 4 word || must be set to 0 to disable servo pulses
        self.servo5H = 0x00 #servo 5 word || must be set to 0 to disable servo pulses
        self.servo5L = 0x00 #servo 5 word || must be set to 0 to disable servo pulses
        self.adV = 0x32 # 0-255 default 50
        self.impSH = 0x00 #impact sensitivy word
        self.impSL = 0x00 #impact sensitivy word
        self.lowBH = 0x02 #low battery word || must be between 550 - 3000
        self.lowBL = 0x32 #low battery word || must be between 550 - 3000
        self.i2C = 0x07 #range 0 - 127 default 0x07
        self.clk = 0x00 # 0 = 100khz 1=400khz
        
        #status packet values
        self.sB =  0xF0 #start packet 240 decimal
        self.errFlag = 0x00 #0 means last command packet is okay
        self.batteryVH = 0x00 # upper byte voltage
        self.batteryVL = 0x00 # lower byte voltage
        self.leftMotorCH = 0x00
        self.leftMotorCL = 0x00
        self.leftEncoderCountH = 0x00
        self.leftEncoderCountL = 0x00
        self.rightMotorCH = 0x00
        self.rightMotorCL = 0x00
        self.rightEncoderCountH = 0x00
        self.rightEncoderCountL = 0x00
        self.accXH = 0x00
        self.accXL = 0x00
        self.accYH = 0x00
        self.accYL = 0x00
        self.accZH = 0x00
        self.accZL = 0x00
        self.impXH = 0x00
        self.impXL = 0x00
        self.impYH = 0x00
        self.impYL = 0x00
        self.impZH = 0x00
        self.impZL = 0x00
        
        self.statusPacket = [
            self.sB,
            self.errFlag,
            self.batteryVH,
            self.batteryVL,
            self.leftMotorCH,
            self.leftMotorCL,
            self.leftEncoderCountH,
            self.leftEncoderCountL,
            self.rightMotorCH,
            self.rightMotorCL,
            self.rightEncoderCountH,
            self.rightEncoderCountL,
            self.accXH,
            self.accXL,
            self.accYH,
            self.accYL,
            self.accZH,
            self.accZL,
            self.impXH,
            self.impXL,
            self.impYH,
            self.impYL,
            self.impZH,
            self.impZL
        ]
        
        print("Setting initial State...")
        self.write_block()
        sleep(2)
        print("Set")
        #self.setMotors(0)
        #self.write_block()
        
    def hexByte(self, value):
        low = value & 0xff
        high = (value >> 8) & 0xff
        return hex(high), hex(low)

    def write_block(self):
        
        commandPacket = [
            self.sb,
            self.pwm,
            self.lmH,
            self.lmL,
            self.lmB,
            self.rmH,
            self.rmL,
            self.rmB,
            self.servo0H,
            self.servo0L,
            self.servo1H,
            self.servo1L,
            self.servo2H,
            self.servo2L, 
            self.servo3H,
            self.servo3L,
            self.servo4H,
            self.servo4L,
            self.servo5H,
            self.servo5L,
            self.adV,
            self.impSH,
            self.impSL,
            self.lowBH,
            self.lowBL,
            self.i2C,
            self.clk
        ]
    
        try:
            print("Writing Data Block")
            j=0
            for i in commandPacket:
                print("writing "+ str(i) + " to reg " + str(j))
                self.bus.write_byte(self.tRexSlaveAddress, j, i)
                j+=1
            
            #self.bus.write_i2c_block_data(self.tRexSlaveAddress, 0x01, commandPacket)
            sleep(0.2)
        except IOError as e:
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))

    #toDo: assign each staus packet a value and provide fuctions for data out of each
    def __i2c_status_packet(self):
        
        for i in range(0,self.num_encoder_ports,1):
            print("reading "+ str(i) + " to reg " + str(j))
            try:
                self.statusPacket[i] = self.bus.read_byte(self.tRexSlaveAddress, j, i)
            except IOError as e:
                print('I/O error({0}): {1}'.format(e.errno, e.strerror))
            j+=1
        
    def read_packet(self,id):
        return self.statusPacket[id]
     
    def update_status(self):
        self.__i2c_status_packet()
        sleep(0.2)

    def print_packet(self):
        try:
            packet = self.bus.i2c_block_data(self.tRexSlaveAdress, 0x00, self.num_encoder_ports)
        except IOError as e:
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))
        ts = str(datetime.now())
        sleep(0.2)
        print packet, ts.rjust(24,'.')

    def setTRexSlave(self, value):
            self.tRexSlaveAddress = value
    def setI2C(self, value):
            self.i2c = value
            
    def setLeftMotor(self, value):
        high,low = self.hexByte(value)
        self.lmH = high
        self.lmL = low
    def setRightMotor(self, value):
        high,low = self.hexByte(value)
        self.rmH = high
        self.rmL = low        
    
    def setMotors(self, value):
        self.setRightMotor(value)
        self.setLeftMotor(value)
    
#    def getsB(self):
#        return self.statusPacket[0]
#     def geterrFlag(self):
#         return self.statusPacket[]
#     def getbatteryVH(self):
#         return self.statusPacket[]
#     def getbatteryVL(self):
#         return self.statusPacket[]
#     def getleftMotorCH(self):
#         return self.statusPacket[]
#     def getleftMotorCL(self):
#         return self.statusPacket[]
#     def getleftEncoderCountH(self):
#         return self.statusPacket[]
#     def getleftEncoderCountL(self):
#         return self.statusPacket[]
#     def getrightMotorCH(self):
#         return self.statusPacket[]
#     def getrightMotorCL(self):
#         return self.statusPacket[]
#     def getrightEncoderCountH(self):
#         return self.statusPacket[]
#     def getrightEncoderCountL(self):
#         return self.statusPacket[]
#     def getaccXH(self):
#         return self.statusPacket[]
#     def getaccXL(self):
#         return self.statusPacket[]
#     def getaccYH(self):
#         return self.statusPacket[]
#     def getaccYL(self):
#         return self.statusPacket[]
#     def getaccZH(self):
#         return self.statusPacket[]
#     def getaccZL(self):
#         return self.statusPacket[]
#     def getimpXH(self):
#         return self.statusPacket[]
#     def getimpXL(self):
#         return self.statusPacket[]
#     def getimpYH(self):
#         return self.statusPacket[]
#     def getimpYL(self):
#         return self.statusPacket[]
#     def getimpZH(self):
#         return self.statusPacket[]
#     def getimpZL(self):
#         return self.statusPacket[]
#         
        


