
from libs.hardware_interface.base_interface import BaseInterface

class SimulatedMotorController:
    def __init__(self, throttle):
        self.throttle = 0.


class SimulatedMotorDriver:
    def __init__(self, throttle):
        self.motor3 = SimulatedMotorController(throttle)
        self.motor4 = SimulatedMotorController(throttle)


class SimulatedMotorControllerInterface(BaseInterface):
    
    def get_interface(self):
        return SimulatedMotorDriver(self.config["throttle"])
