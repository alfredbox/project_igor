from busio import I2C
from board import SDA, SCL
import time

from modules.module_base import ModuleBase

import adafruit_bno055


class ImuReadModule(ModuleBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 0.002
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        self.imu_state = state.imu_state
        self.sensor = adafruit_bno055.BNO055(I2C(SCL, SDA))

    def step(self):
        angle_y = self.sensor.euler[1]
        if angle_y is not None:
            self.imu_state.angle_y = angle_y
