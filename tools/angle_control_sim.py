import json
import logging
import math
import time

from libs.clamp import clamp
import libs.logger_setup as logger_setup
from libs.pid import PID

logger_setup.setup(sim=True)
logger = logger_setup.get_logger()

class AngleControlSim:
    def __init__(self, kd, ki, kp, dt):
        self.angle_control = PID(kd, ki, kp)
        self.angle_control.set_point(0.)
        self.dt = dt

    def sim_forward_for(self, secs, angle):
        starting = time.monotonic()
        elapsed = 0
        while(elapsed < secs):
            a = self.angle_fcn(angle, elapsed)
            signal = self.angle_control.signal(a)
            t = time.monotonic()
            if logger.getEffectiveLevel() <= logging.DEBUG:
                data = {
                    'timestamp': t,
                    'set_throttle': signal,
                    'control_angle': a
                }
                logger.debug('Control Data: {}'.format(json.dumps(data)))
            elapsed = t - starting
            time.sleep(self.dt)

    def angle_fcn(self, angle_0, elapsed):
        return math.sin(elapsed*2)*angle_0
                
if __name__ == "__main__":
    #kp 0.05 - 0.08
    #ki 0.01 - 0.2
    #kd 0.01 - 0.1
    sim = AngleControlSim(0.04, 0.04, 0.04, 0.006)
    sim.sim_forward_for(3., -10.)

