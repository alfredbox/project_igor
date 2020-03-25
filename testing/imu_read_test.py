import state
import time
import executor

import modules.imu_read as imu_read
import modules.state_printer as state_printer

def helper_assemble_modules(state):
    modules = [
        state_printer.StatePrintModule(state),
        TestImuReadModule(state)
    ]
    return modules
        

class TestImuReadModule(imu_read.ImuReadModule):
    def __init__(self, state):
        super().__init__(state)

    def step(self):
        angle_y = self.sensor.euler[1]
        if angle_y is not None:
            self.imu_state.angle_y = angle_y
            self.imu_state.angle_history.append((angle_y, time.time()))

s = state.State()
modules = helper_assemble_modules(s)
executor.execute(modules)
