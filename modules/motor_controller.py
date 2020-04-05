import time
from libs.clamp import clamp
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
        self.controller.throttle = self._deadband_rm(val)
        self.motor_state.throttle = val

    def _deadband_rm(self, val):
        '''Remove deadband to linearize response.
        Motor response to the throttle is mostly linear save for a deadband
        between +-0.3 this removes that deadband to linearize the response.
        '''
        offset = 0 if val == 0 else 0.28*val/abs(val)
        return clamp(val*0.72 + offset)
        
class MotorControlModule(ModuleBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 0.002
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        self.data = []
        self.start_time = time.time()
        
        kit = MotorKit()
        self.drive_state = state.drive_state
        # Port Motor
        self.port_motor = MotorControl(self.drive_state.port_motor, kit.motor3)
        # Starboard Motor
        self.sbrd_motor = MotorControl(self.drive_state.sbrd_motor, kit.motor4)
        self.angle_control = PID(0.08, 0.08, 0.0011)
        self.angle_control.set_point(0.)
        #self.angle_control = PID(0.0550, 0.627, 0.002)


    def step(self):
        # TODO make less trivial
        angle = self.state.imu_state.angle_y
        signal = self.angle_control.signal(-angle)
        self.port_motor.set_throttle(signal)
        self.sbrd_motor.set_throttle(signal)
        t = time.time()
        if t - self.start_time > 80:
            raise ValueError('No values')
        self.data.append((t, angle, signal))

    def cleanup(self):
        self.port_motor.set_throttle(0)
        self.sbrd_motor.set_throttle(0)
        with open('igor_data_dump.csv', 'w+') as f:
            for d in self.data:
                f.write('{}, {}, {}\n'.format(d[0], d[1], d[2]))
        
