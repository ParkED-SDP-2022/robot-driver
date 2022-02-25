import BenchOS.firmware.MotorControllers.motors
from motors import *

m = Motors()

try:
    m.update_status()
    m.read_packet(1)
    sleep(0.2)

except:
    print("bus error")
