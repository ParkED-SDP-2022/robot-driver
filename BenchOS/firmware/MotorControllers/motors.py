#!/usr/bin/python

import os
import time
import numpy as np
from smbus2 import SMBus, i2c_msg
from time import sleep
from datetime import datetime

class Motors(object):
    def __init__(self):

        print("Starting SMBus . . .")
        self.bus = SMBus(1)
        self.msg = i2c_msg()
        sleep(2)
        print("SMBus Started.")
        self.tRexSlave = 0x07
        self.num_reg = 24 #d5 & d6 for motors

        self.sysPause = False

        #command packet values
        self.sb = 0x0f #start Byte
        self.pwm = 0x06 #motor pwm frequency 0-7
        self.lmH = 0x00 #left motor speed word || -255 to max 255
        self.lmL = 0x00 #left motor speed word || -255 to max 255
        self.lmB = 0x00 #left motor break || 0 or 1
        self.rmH = 0x00 #right motor speed word || max 255
        self.rmL = 0x00 #right motor speed word || max 255
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
        self.clk = 0x01 # 0 = 100khz 1=400khz

        self.statusPacket = []

    def i2cRead(self):
        try:
            read = self.msg.read(self.tRexSlave, self.num_reg)
            self.bus.i2c_rdwr(read)
            sleep(0.2)
            self.statusPacket = list(read)
        except IOError as e:
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))

    def i2cWrite(self):
        cmd = self.updateCMD()
        try:
            self.bus.write_i2c_block_data(self.tRexSlave, 0x0f, cmd)
        except IOError as e:
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))
        sleep(0.2)


    def print_packet(self):
        ts = str(datetime.now())
        print(self.statusPacket, ts.rjust(24,'.'))

    def updateCMD(self):
        commandPacket = [self.pwm,self.lmH,self.lmL,self.lmB,self.rmH,
                        self.rmL,self.rmB,self.servo0H,self.servo0L,self.servo1H,
                        self.servo1L,self.servo2H,self.servo2L,self.servo3H,
                        self.servo3L,self.servo4H,self.servo4L,self.servo5H,
                        self.servo5L,self.adV,self.impSH,self.impSL,self.lowBH,
                        self.lowBL,self.i2C,self.clk]
                        
        print("packet updated")
        return commandPacket

    def setTRexSlave(self, value):
        print("old slave = " + str(self.tRexSlave))
        self.tRexSlave = value
        print("new slave = "+ str(value))

    def setsB(self, value):
        print("old sb = " + str(self.sb))
        self.sb = value
        print("new sb = "+ str(value))

    def setLeftMotor(self, value):
        if value>255:
            value=255
        elif value<-255:
            value=-255
        high,low = self.hexByte(value)
        self.lmH = high
        self.lmL = low
    def setRightMotor(self, value):
        if value>255:
            value=255
        elif value<-255:
            value=-255
        high,low = self.hexByte(value)
        self.rmH = high
        self.rmL = low

    def setMotors(self, value):
        self.setRightMotor(value)
        self.setLeftMotor(value)
        print("set Motors")
        self.i2cWrite()

    def hexByte(self, value):
        low = value & 0xff
        high = (value >> 8) & 0xff
        return high, low

    def byteHex(self, value1, value2):
        a = value1
        b = a << 8 | value2
        return b

    def getsB(self):
        return self.statusPacket[0]

    def geterrFlag(self):
        return self.statusPacket[1]

    def getbatteryV(self):
        return self.byteHex(self.statusPacket[2], self.statusPacket[3])

    def getleftMotorC(self):
        return self.byteHex(self.statusPacket[4], self.statusPacket[5])

    def getleftEncoderCount(self):
        return self.byteHex(self.statusPacket[6], self.statusPacket[7])

    def getrightMotorC(self):
        return self.byteHex(self.statusPacket[8], self.statusPacket[9])

    def getrightEncoderCount(self):
        return self.byteHex(self.statusPacket[10], self.statusPacket[11])

    def getaccX(self):
        return self.byteHex(self.statusPacket[12], self.statusPacket[13])

    def getaccY(self):
        return self.byteHex(self.statusPacket[14], self.statusPacket[15])

    def getaccZ(self):
        return self.byteHex(self.statusPacket[16], self.statusPacket[17])

    def getimpX(self):
        return self.byteHex(self.statusPacket[18], self.statusPacket[19])

    def getimpY(self):
        return self.byteHex(self.statusPacket[20], self.statusPacket[21])

    def getimpZ(self):
        return self.byteHex(self.statusPacket[22], self.statusPacket[23])

    def pause(self):
        self.sysPause = True
    def resume(self):
        self.sysPause = False

    # def main(self):
        # while True:
            # if self.sysPause == False:
                # self.i2cWrite()
                # sleep(0.1)
                # self.i2cRead()
            # else:
                # sleep(0.1)




