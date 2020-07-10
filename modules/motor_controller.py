import json
import logging
import time

from libs.clamp import clamp
from libs.logger_setup import get_logger
from libs.pid import PID

from modules.module_base import ModuleBase

logger = get_logger()


class ControlTooSlow(Exception):
    pass


class MotorControl:
    def __init__(self, motor_state, controller, offset):
        self.controller = controller
        self.motor_state = motor_state
        self.offset = offset

    def set_throttle(self, val):
        assert (val <= 1. and val >= -1.), (
            "Throttle must be between -1.0 and 1.0")
        self.controller.throttle = self._deadband_rm(val)
        self.motor_state.throttle = val

    def _deadband_rm(self, val):
        '''Remove deadband to linearize response.
        Motor response to the throttle is mostly linear save for a deadband
        between +-self.offset this removes that deadband to linearize 
        the response.
        '''
        offset = 0 if val == 0 else self.offset*val/abs(val)
        return clamp(val*(1.-self.offset) + offset)
       

class MotorControlModule(ModuleBase):
    def __init__(self, state, simulated_motor_driver=None):
        DEFAULT_CADENCE_S = 0.002
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        self.start_time = time.time()
        self.last_control_time = None

        if simulated_motor_driver is not None:
            # Running in offlinse sim mode
            kit = simulated_motor_driver
        else:
            # Running in online mode
            # Online only imports #
            from adafruit_motorkit import MotorKit
            ######################
            kit = MotorKit()
        self.drive_state = state.drive_state
        # Port Motor
        self.port_motor = MotorControl(
                self.drive_state.port_motor, 
                kit.motor3,
                0.25)
        # Starboard Motor
        self.sbrd_motor = MotorControl(
                self.drive_state.sbrd_motor, 
                kit.motor4,
                0.2)
        self.angle_control = PID(0.13, 0.275, 0.0075, name='angle_pid')
        self.angle_control.set_point(0.0)
        self.speed_control = PID(0.0, 0.05, 0.0, lo=-2.5, hi=2.5, name='speed_pid')
        self.speed_control.set_point(0.0)

    def step(self):
        if not self.state.imu_state:
            return
        # Speed Control
        average_speed = ((self.drive_state.port_motor.rpm + 
                          self.drive_state.sbrd_motor.rpm) / 2.0)
        average_speed = average_speed if self.drive_state.port_motor.direction else -average_speed
        speed_signal = self.speed_control.signal(average_speed)
        # Angle Control
        self.angle_control.set_point(-speed_signal)
        angle = self.state.imu_state.angle_y
        d_angle = self.state.imu_state.d_angle_y
        angle_signal = self.angle_control.signal(-angle, -d_angle)
        self.port_motor.set_throttle(angle_signal)
        self.sbrd_motor.set_throttle(angle_signal)
        t = time.time()
        dt = (t - self.last_control_time 
              if self.last_control_time is not None 
              else self.last_control_time)
        self.last_control_time = t
        if logger.getEffectiveLevel() <= logging.DEBUG:
            data = {
                'timestamp': t,
                'set_throttle': angle_signal,
                'control_angle': angle,
                'control_d_angle': d_angle
            }
            logger.debug('Control Data: {}'.format(json.dumps(data)))
        
        if dt is not None and dt > 0.05:
            msg = 'Duration since last control is too high ({} s)'.format(dt)
            logger.error(msg)
            #raise ControlTooSlow('msg')


    def cleanup(self):
        self.port_motor.set_throttle(0)
        self.sbrd_motor.set_throttle(0) 
