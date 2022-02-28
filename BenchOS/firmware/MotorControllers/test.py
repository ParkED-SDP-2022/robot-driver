import BenchOS.firmware.MotorControllers.motors
from motors import *

m = Motors()

print("Getting initial State...")
print("\n")

m.print_packet()
sleep(0.2)
        
#print("testing Hex of 400")
#u,l = m.hexByte(400)
#print(u)
#print(l)

#print("back to int")
#print(m.byteHex(u,l))

#print("testing integer of 0x10 and 0x12")
#print(m.byteHex(0x10,0x12))


print("getting filled command")
print(m.update_Command())
sleep(0.2)

m.write_block()

for i in range(0,100,1):
    m.update_Command()
    m.write_block()
    m.read_packet()
    print(m.geterrFlag())

# print("updating packet")
# m.read_packet()

# print("start Byte")
# print(m.getsB())

# print("error Flag")
# print(m.geterrFlag())

# print("battery voltage cV")
# print(m.getbatteryV())

# print("left motor current mA")
# print(m.getleftMotorC())

# print("left motor count ")
# print(m.getleftEncoderCount())

# print("right motor current mA")
# print(m.getrightMotorC())

# print("right motor count ")
# print(m.getrightEncoderCount())

# print("acceleration x")
# print(m.getaccX())

# print("acceleration y")
# print(m.getaccY())

# print("acceleration z ")
# print(m.getaccZ())

# print("impact x ")
# print(m.getimpX())

# print("impact y")
# print(m.getimpY())

# print("impact z ")
# print(m.getimpZ())
