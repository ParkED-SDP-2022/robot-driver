import math
import sys
import time
from grove.adc import ADC
 
 
class FSR(ADC):
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
 
    @property
    def value(self):
        return self.adc.read(self.channel)
 
 
Grove = FSR
 
 
def main():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)
 
    sensor = FSR(int(sys.argv[1]))
 
    while True:
        print('Slide potentiometer value: {}'.format(sensor.value))
        time.sleep(.2)
 
 
if __name__ == '__main__':
    main()
