import adafruit_bno055
from busio import I2C
from board import SDA, SCL
import time

from libs.hardware_interface.base_interface import BaseInterface


class ImuInterface(BaseInterface):

    def get_interface(self):
        sensor = adafruit_bno055.BNO055(I2C(SCL, SDA))
        # read until sensor activates
        e = 0
        while e==0:
            e = sensor.euler[1]
            time.sleep(0.1)
        # TODO raise on too many its
        return sensor
