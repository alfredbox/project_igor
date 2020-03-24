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
        motor_compute.MotorCompute(state),
        state_printer.StatePrinter(state),
        TestMotorController(state)
    ]
    return modules
        

class TestMotorController(motor_controller.MotorModule):
    def __init__(self, state):
        super().__init__(state)
        # TODO other things (ALF)
        self.time = time.time()

    def control_policy(self):
        # TODO (ALF)
        val = 0.
        if (time.time() - self.time) > 1:
            val=0.5
        if (time.time() - self.time) > 10:
            val=0.8
        if (time.time() - self.time) > 20:
            val=0

        self.port_motor.set_throttle(val)
        self.sbrd_motor.set_throttle(val)

s = state.State()
modules = helper_assemble_modules(s)
executor.execute(modules)
