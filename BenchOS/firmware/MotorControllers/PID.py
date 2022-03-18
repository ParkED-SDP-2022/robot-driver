class PID():

    def __init__(self):
        # initialize stored data
        self.e_prev = 0
        self.t_prev = 0
        self.I = 0
        self.Kp = 0
        return

    def PID(Kp, Ki, Kd, MV_Bar=80):

        # initial control
        MV = MV_Bar
        self.Kp = Kp
        #enc
        #acc
        #cur

        #vel | 0-255 | cruise 80 | moves 130
        while True:
            # yield MV, wait for new t, PV, SP
            t, PV, SP = yield MV

            # PID calculations
            e = enc - encT # e is error from accel and encoder - error should be velocity | curr vel - target

            P = Kp * e #need to be multiplied by motor output - try use this only
            I = I + Ki * e * (t - t_prev) #use 3rd
            D = Kd * (e - e_prev) / (t - t_prev) #use second

            MV = P #+ I + D

            # update stored data for next iteration
            e_prev = e
            t_prev = t
