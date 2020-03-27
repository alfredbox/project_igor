
from libs.pid import PID
from modules.module_base import ModuleBase

from adafruit_motorkit import MotorKit

class MotorControl:
    def __init__(self, motor_state, controller):
        self.controller = controller
        self.motor_state = motor_state

    def set_throttle(self, val):
        assert (val <= 1. and val >= -1.), (
            "Throttle must be between -1.0 and 1.0")
        self.controller.throttle = val
        self.motor_state.throttle = val
        
class MotorControlModule(ModuleBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 0.002
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        
        kit = MotorKit()
        self.drive_state = state.drive_state
        # Port Motor
        self.port_motor = MotorControl(self.drive_state.port_motor, kit.motor3)
        # Starboard Motor
        self.sbrd_motor = MotorControl(self.drive_state.sbrd_motor, kit.motor4)
        self.goal_angle = 0
        self.angle_control = PID(0.15, 0., -0.02)
        #self.angle_control = PID(0.0550, 0.627, 0.002)


    def step(self):
        # TODO make less trivial
        angle = self.state.imu_state.angle_y
        signal = self.angle_control.signal(angle)
        signal = min(signal, 1)
        signal = max(signal, -1)
        self.port_motor.set_throttle(signal)
        self.sbrd_motor.set_throttle(signal)

    def cleanup(self):
        self.port_motor.set_throttle(0)
        self.sbrd_motor.set_throttle(0)
