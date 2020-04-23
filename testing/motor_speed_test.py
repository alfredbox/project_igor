import state
import executor

import libs.logger_setup as logger_setup
import modules.motor_read as motor_read
import modules.motor_compute as motor_compute
import modules.state_printer as state_printer
from testing.helpers import TestMotorController

# Logging
logger_setup.setup(sim=True)
logger = logger_setup.get_logger()

def helper_assemble_modules(state):
    modules = [
        motor_read.MotorReadModule(state),
        motor_compute.MotorComputeModule(state),
        state_printer.StatePrintModule(state),
        TestMotorController(state)
    ]
    return modules


s = state.State()
modules = helper_assemble_modules(s)
executor.execute(modules)
