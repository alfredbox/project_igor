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
        # TODO other things (ALF)
        self.time = time.time()
        self.val = 1

    def step(self):
        # TODO (ALF)
        if (time.time() - self.time) > 15:
            self.val -= 0.05
            self.time = time.time()

        self.port_motor.set_throttle(self.val)
        self.sbrd_motor.set_throttle(self.val)

