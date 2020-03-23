import state
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
        super.__init__(state)
        # TODO other things (ALF)

    def control_policy(self):
        # TODO (ALF)
        pass

s = state.State()
modules = helper_assemble_modules(s)
executor.execute(modules)
