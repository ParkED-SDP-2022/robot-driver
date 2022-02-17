import grove_compass_lib
import time

class CompassData():
    
    def __init__(self):
        
        self.c=grove_compass_lib.compass()
        
    def getData(self):
        self.c.update()
        return self.c.x, self.c.y, self.c.z, self.c.headingDegrees
    
    def getUpdate(self):
        self.c.update()
        print "X:",self.c.x,"Y:",self.c.y,"X:",self.c.z,"Heading:",self.c.headingDegrees
    
    def getX(self):
        self.c.update()
        return self.c.x
    
    def getY(self):
        self.c.update()
        return self.c.y
    
    def getZ(self):
        self.c.update()
        return self.c.z
    
    def getHeadng(self):
        self.c.update()
        return self.c.headingDegrees
