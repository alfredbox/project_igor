from adafruit_motorkit import MotorKit
from libs.hardware_interface.base_interface import BaseInterface


class MotorControllerInterface(BaseInterface):
    def get_interface(self):
        kit = MotorKit()
        return kit
