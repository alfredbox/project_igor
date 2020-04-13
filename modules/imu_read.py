from busio import I2C
from board import SDA, SCL
import json
import logging
import time

from libs.logger_setup import get_logger
from modules.module_base import ModuleBase

import adafruit_bno055


logger = get_logger()


class ImuReadTooSlow(Exception):
    pass

class TipTooFar(Exception):
    pass


class ImuReadModule(ModuleBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 0.002
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        self.imu_state = state.imu_state
        self.sensor = adafruit_bno055.BNO055(I2C(SCL, SDA))
        self.unrecoverable = 20.
        self.last_poll_time = None
        self.last_angle_y = None

    def step(self):
        angle_y = self.sensor.euler[1]
        if angle_y is not None:
            self.imu_state.angle_y = angle_y
            d_angle_y = (None if self.last_angle_y is not None 
                         else angle_y - self.last_angle_y)
            self.last_angle_y = angle_y
            t = time.time()
            dt = (t - self.last_poll_time if
                  self.last_poll_time is not None
                  else self.last_poll_time)
            self.last_poll_time = t
            if d_angle_y is not None and dt is not None:
                self.imu_state.d_angle_y = 0.9 * self.imu_state.d_angle_y + 0.1*d_angle_y/dt
            if logger.getEffectiveLevel() <= logging.DEBUG:
                data = {
                    'timestamp': t,
                    'measured angle': angle_y
                }
                logger.debug('IMU Data: {}'.format(json.dumps(data)))
            if dt is not None and dt > 0.05:
                msg = ('Duration since last IMU read is too high'
                       ' ({} s)'.format(dt))
                logger.error(msg)
                #raise ImuReadTooSlow(msg)
            if abs(angle_y) > self.unrecoverable:
                msg = 'igor tipped too far ({} degs)'.format(angle_y)
                logger.error(msg)
                raise TipTooFar(msg)
