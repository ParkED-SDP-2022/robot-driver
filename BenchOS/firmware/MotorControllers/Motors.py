#!/usr/bin/python3

import time
import serial
from time import sleep

class Motors(object):
    def __init__(self):

        i=0
        self.arduino = None
        while self.arduino == None:
            try:
                self.arduino = serial.Serial(port='/dev/ttyACM'+str(i), baudrate=9600, timeout=0.1)
                print(i)
                print(self.arduino)
            except:
                i+=1
        sleep(2)
        
        #command packet values
        self.sb = 0x0f #start Byte
        self.pwm = 0x07 #motor pwm frequency 0-7
        self.lm = 0x00 #left motor speed Byte || -255 to max 255
        self.lmB = 0x00 #left motor break || 0 or 1
        self.rm = 0x00 #right motor speed Byte || max 255
        self.rmB = 0x00 #right motor break || 0 or 1
        self.servo0 = 0x00 #servo 0 Byte
        self.servo1 = 0x00 #servo 1 Byte
        self.servo2 = 0x00 #servo 2 Byte
        self.servo3 = 0x00 #servo 3 Byte
        self.servo4 = 0x00 #servo 4 Byte || must be set to 0 to disable servo pulses
        self.servo5 = 0x00 #servo 4 Byte || must be set to 0 to disable servo pulses
        self.adV = 0x32 # 0-255 default 50
        self.impS = 0x32 #impact sensitivy word deault 50 | range 0 to 1023
        self.lowB = 0x410 #low battery word || must be between 550 - 3000
        self.i2C = 0x07 #range 0 - 127 default 0x07
        self.clk = 0x01 # 0 = 100khz 1=400khz

        self.statusPacket = []

    def updateCMD(self):
        commandPacket = [self.sb,self.pwm,self.lm,self.lmB,self.rm,self.rmB,self.servo0,self.servo1,self.servo2,self.servo3,self.servo4,self.servo5,self.adV,self.impS,self.lowB,self.i2C,self.clk]

        cmd = [str(element) for element in commandPacket]
        cmdStr = (",".join(cmd))+"\n"

        return cmdStr

    def setTRexSlave(self, value):
        print("old slave = " + str(self.tRexSlave))
        self.tRexSlave = value
        print("new slave = "+ str(value))

    def setStartByte(self, value):
        print("old sb = " + str(self.sb))
        self.sb = value
        print("new sb = "+ str(value))

    def setPWM(self, value):
        print("old pwm = " + str(self.sb))
        self.pwm = value
        print("new pwm = " + str(value))

    def setLowBattery(self, value):
        print("old lowB = " + str(self.sb))
        self.lowB = value
        print("new lowB = " + str(value))

    def setImpS(self, value):
        print("old impS = " + str(self.sb))
        self.impS = value
        print("new impS = " + str(value))

    def setAdv(self, value):
        print("old adv = " + str(self.sb))
        self.adv = value
        print("new adv = " + str(value))


    #--------------------------------------------------------------------------------------------
    #motor control functions
    def __setLeftMotor(self, speed):
        self.lmB = 0
        self.lm = speed
    def __setRightMotor(self, speed):
        self.rmB = 0
        self.rm = speed

    def setMotors(self, speed, angularVel):
        self.lmB = 0
        self.rmB = 0
        
        if (speed+angularVel) > 255 or (speed+angularVel) < -255:
            speed = speed - angularVel
        if speed >255 and angularVel == 0:
            speed = 255
        if speed <-255 and angularVel == 0:
            speed = -255
            
        # Angular velocity of 1 means we shift the linear velocity to right wheel +1
        if speed >=0:
            self.__setRightMotor(speed+ angularVel*-1)
            self.__setLeftMotor(speed+ angularVel)
        else:
            self.__setRightMotor(speed + angularVel)
            self.__setLeftMotor(speed + angularVel * -1)

    def stopMotors(self):
        self.lmB = 1
        self.rmB = 1
        self.setMotors(0,0)

    #--------------------------------------------------------------------------------------------
    #hex value calculations to provide

    def hexByte(self, value):
        low = value & 0xff
        high = (value >> 8) & 0xff
        return high, low

    def byteHex(self, value1, value2):
        a = value1
        b = a << 8 | value2
        return b

    #--------------------------------------------------------------------------------------------

    #getter functions to retrieve individual packet info

    def getsB(self):
        return self.statusPacket[0]

    def geterrFlag(self):
        return self.statusPacket[1]

    def getbatteryV(self):
        return self.statusPacket[2]

    def getleftMotorC(self):
        return self.statusPacket[3]

    def getleftEncoderCount(self):
        return self.statusPacket[4]

    def getrightMotorC(self):
        return self.statusPacket[5]

    def getrightEncoderCount(self):
        return self.statusPacket[6]

    def getaccX(self):
        return self.statusPacket[7]

    def getaccY(self):
        return self.statusPacket[8]

    def getaccZ(self):
        return self.statusPacket[9]

    def getimpX(self):
        return self.statusPacket[10]

    def getimpY(self):
        return self.statusPacket[11]

    def getimpZ(self):
        return self.statusPacket[12]

    #--------------------------------------------------------------------------------------------

    def write_read(self):
        cmd = self.updateCMD()
        self.arduino.reset_input_buffer()
        self.arduino.reset_output_buffer()
        self.arduino.write(bytearray(cmd, "utf-8"))
        output = []
        input_from_serial = self.arduino.readline()
        string = input_from_serial.split(',')
        for i in range(0, len(string)-1, 1):
            output.append(int(string[i]))
        time.sleep(0.1)
        return output

    #--------------------------------------------------------------------------------------------




