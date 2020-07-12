from gpiozero import DigitalInputDevice

from libs.hardware_interface.base_interface import BaseInterface

class MotorEncoderInterface(BaseInterface):
    def get_interface(self):
        return DigitalInputDevice(self.config["pin"])
