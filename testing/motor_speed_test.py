import state
import time
import executor

import modules.motor_read as motor_read
import modules.motor_compute as motor_compute
import modules.motor_controller as motor_controller
import modules.state_printer as state_printer

def helper_assemble_modules(state):
    modules = [
        motor_read.MotorReadModule(state),
        motor_compute.MotorComputeModule(state),
        state_printer.StatePrintModule(state),
        TestMotorController(state)
    ]
    return modules
        

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

s = state.State()
modules = helper_assemble_modules(s)
executor.execute(modules)
