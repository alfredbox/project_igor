import time

class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.error = 0
        self.i_error = 0
        self.setpoint = -0.5
        self.last_point = 0
        self.time = time.time()

    def signal(self, value):
        dt = time.time() - self.time
        #import pdb
        #pdb.set_trace()
        error = value - self.setpoint
        self.i_error += error*dt
        self.i_error = min(self.i_error, 0.7)
        self.i_error = max(self.i_error, -0.7)
        signal =(self.Kp*error 
                 + self.Ki*self.i_error
                 - self.Kd*(value-self.last_point)/dt)
        self.error = error
        self.last_point = value
        self.time += dt
        return signal
