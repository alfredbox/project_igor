import time

import modules.motor_controller as motor_controller
import modules.module_base as module_base


class TestMotorController(motor_controller.MotorControlModule):
    def __init__(self, state):
        super().__init__(state)
        self.time = time.time()
        self.val = -1

    def step(self):
        if (time.time() - self.time) > 15:
            self.val += 0.05
            self.time = time.time()
        if self.val >= 1:
            self.state.execution_control.termination_requested = True

        self.port_motor.set_throttle(self.val)
        self.sbrd_motor.set_throttle(self.val)


class TestMotorControllerBasic(motor_controller.MotorControlModule):
    def __init__(self, state):
        super().__init__(state)
        self.val = 0.5

    def step(self):
        self.port_motor.set_throttle(self.val)
        self.sbrd_motor.set_throttle(self.val)


class Terminator(module_base.ModuleBase):
    def __init__(self, state, term_after_s=15):
        super().__init__(state, cadence=term_after_s)

    def step(self):
        self.state.execution_control.termination_requested = True

