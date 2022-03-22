from time import sleep
from pySerialTransfer import pySerialTransfer as txfer


class struct(object):
  dre = 0
  dle = 0
  pid_params = False
  kp_l = 2
  ki_l = 1.3
  kd_l = 0.1
  kp_r = 2
  ki_r = 1.3
  kd_r = 0.1


if __name__ == '__main__':
    try:
        tuningPacket = struct
        link = None
        i = 0
        while link == None:
            try:
                link = txfer.SerialTransfer('/dev/ttyACM'+str(i))
            except:
                i += 1

        
        
        link.open()
        sleep(5)
    
        while True:

            while True:
                dre = raw_input('Desired Right Encoder Count')
                if dre >= 0 and dre <=120:
                    tuningPacket.dre = dre
                    break
                else:
                    print('invalid value for dre entered: {}'.format(dre))
            while True:
                dle = raw_input('Desired Left Encoder Count')
                if dle >= 0 and dle <=120:
                    tuningPacket.dle = dle
                    break
                else:
                    print('invalid value for dre entered: {}'.format(dle))
            while True:
                ans = raw_input('Tune PID parameters? 1 or 0')
                if ans == 1:
                    tuningPacket.pid_params = True
                    break
                elif ans == 0:
                    tuningPacket.pid_params = False
                else:
                    print('invalid value entered: {}'.format(ans))


            sendSize = 0
            
            sendSize = link.tx_obj(tuningPacket.dre, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.dle, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.pid_params, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.kp_l, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.ki_l, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.kd_l, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.kp_r, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.ki_r, start_pos=sendSize)
            sendSize = link.tx_obj(tuningPacket.kd_r, start_pos=sendSize)
            link.send(sendSize)
                
        
    except KeyboardInterrupt:
        tuningPacket.dle = 0
        tuningPacket.dre = 0
        tuningPacket.pid_params = False
        sendSize = 0    
        sendSize = link.tx_obj(tuningPacket.dre, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.dle, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.pid_params, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.kp_l, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.ki_l, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.kd_l, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.kp_r, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.ki_r, start_pos=sendSize)
        sendSize = link.tx_obj(tuningPacket.kd_r, start_pos=sendSize)
        link.send(sendSize)
        link.close()