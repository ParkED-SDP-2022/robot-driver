import time, sys, signal, atexit, math
try:
    from upm import pyupm_bmm150 as sensorObj
except ImportError:
    print('Error: Please install python-mraa python-upm module.\r\n' 
          'See instruction here https://github.com/Seeed-Studio/pi_repo#mraa--upm-package-repository-for-raspberry-pi ')
 
 
def main():
    # Instantiate a BMP250E instance using default i2c bus and address
    sensor = sensorObj.BMM150(1, 0x13)
 
 
    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit
 
    # This function lets you run code on exit
    def exitHandler():
        print("Exiting")
        sys.exit(0)
 
    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)
 
    # now output data every 250 milliseconds
    while (1):
        sensor.update()
 
        data = sensor.getMagnetometer()
        print("Magnetometer x: {0:.2f}".format(data[0]), end=' ')
        print(" y: {0:.2f}".format(data[1]), end=' ')
        print(" z: {0:.2f}".format(data[2]), end=' ')
        print(" uT")
 
        xyHeading = math.atan2(data[0], data[1])
        zxHeading = math.atan2(data[2], data[0])
        heading = xyHeading
 
        if heading < 0:
            heading += 2*math.pi
        if heading > 2*math.pi:
            heading -= 2*math.pi
 
        headingDegrees = heading * 180/(math.pi); 
        xyHeadingDegrees = xyHeading * 180 / (math.pi)
        zxHeadingDegrees = zxHeading * 180 / (math.pi)
 
        print('heading(axis_Y point to): {0:.2f} degree'.format(headingDegrees))
        time.sleep(.250)
 
if __name__ == '__main__':
    main()
