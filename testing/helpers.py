import time

import modules.motor_controller as motor_controller

class TaskState:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0


class SimpleState:
    def __init__(self):
        self.task_a = TaskState()
        self.task_b = TaskState()


class TestMotorController(motor_controller.MotorControlModule):
    def __init__(self, state):
        super().__init__(state)
        self.time = time.time()
        self.val = 1

    def step(self):
        if (time.time() - self.time) > 15:
            self.val -= 0.05
            self.time = time.time()
        if self.val < -0.9:
            self.state.execution_control.termination_requested = True

        self.port_motor.set_throttle(self.val)
        self.sbrd_motor.set_throttle(self.val)


class TestMotorControllerBasic(motor_controller.MotorControlModule):
    def __init__(self, state, logging=False):
        super().__init__(state, logging=logging)
        self.time = time.time()
        self.val = 0.5

    def step(self):
        if (time.time() - self.time) > 15:
            self.state.execution_control.termination_requested = True

        self.port_motor.set_throttle(self.val)
        self.sbrd_motor.set_throttle(self.val)
