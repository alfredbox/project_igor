import time

from libs.clamp import clamp   

class PID:
    def __init__(self, Kp, Ki, Kd, lo=-1, hi=1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.lo = lo
        self.hi = hi
        self.i_error = 0.
        self.set_point(0.)
        self.lastpoint = None
        self.time = time.monotonic()

    def set_point(self, point):
        self._setpoint = point

    def setpoint(self):
        return self._setpoint

    def signal(self, value, d_value=None):
        dt = time.monotonic() - self.time
        assert dt > 0, 'Non positive timestep - aborting.'

        error = self.setpoint() - value
        dpoint = 0 if self.lastpoint is None else value - self.lastpoint

        p = self.Kp*error
        self.i_error += self.Ki * error * dt
        self.i_error = clamp(self.i_error, lo=self.lo, hi=self.hi)
        i = self.i_error
        dv_dt = d_value if d_value is not None else dpoint/dt
        d = self.Kd * dv_dt

        # Advance stored data
        self.time += dt
        self.lastpoint = value

        return clamp(p+i-d, lo=self.lo, hi=self.hi)
