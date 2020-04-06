import asyncio
import unittest
import time

import executor
import modules.imu_read as imu_read
import modules.motor_read as motor_read
import modules.motor_compute as motor_compute
import modules.motor_controller as motor_controller
import state
from testing.helpers import TestMotorControllerBasic, Terminator

class TestTimingOneModule(unittest.TestCase):
    def setUp(self):
        self.modules = []
    
    def helper_executor(self, state):
        terminator = Terminator(state, term_after_s=40)
        self.modules.append(terminator)
        executor.execute(self.modules)

    def helper_timing(self, log, duration_tol, cadence_tol):
        self.assertTrue(log)
        last_time = None
        durations = []
        cadences = []
        for ts in log:
            durations.append(ts['ran_for_s'])
            if last_time is not None:
                cadences.append(ts['ran_at_s'] - last_time)
            last_time = ts['ran_at_s']
        self.assertLess(max(durations), duration_tol)
        self.assertLess(max(cadences), cadence_tol)

    def test_motor_controller(self):
        s = state.State()
        mc_module = TestMotorControllerBasic(s)
        mc_module.set_logging(True)
        self.modules.append(mc_module)
        self.helper_executor(s)
        self.helper_timing(mc_module.execution_log, 0.01, 0.05)

    def test_imu_read(self):
        s = state.State()
        imu_module = imu_read.ImuReadModule(s)
        imu_module.set_logging(True)
        self.modules.append(imu_module)
        self.helper_executor(s)
        self.helper_timing(imu_module.execution_log, 0.01, 0.05)

    def test_encoder_read(self):
        s = state.State()
        mr_module = motor_read.MotorReadModule(s)
        mr_module.set_logging(True)
        self.modules.append(mr_module)
        # Need to spin the motors to make sense
        self.modules.append(TestMotorControllerBasic(s))
        self.helper_executor(s)
        self.helper_timing(mr_module.execution_log, 0.01, 5.05)

    def test_motor_compute(self):
        s = state.State()
        mc_module = motor_compute.MotorComputeModule(s)
        mc_module.set_logging(True)
        self.modules.append(mc_module)
        # Need to spin the motors to make sense
        self.modules.append(TestMotorControllerBasic(s))
        self.modules.append(motor_read.MotorReadModule(s))
        self.helper_executor(s)
        self.helper_timing(mc_module.execution_log, 0.01, 0.15)

    def test_major_modules_together(self):
        s = state.State()
        mc_module = motor_controller.MotorControlModule(s)
        mc_module.set_logging(True)
        mr_module = motor_read.MotorReadModule(s)
        mr_module.set_logging(True)
        mx_module = motor_compute.MotorComputeModule(s)
        mx_module.set_logging(True)
        imu_module = imu_read.ImuReadModule(s)
        imu_module.set_logging(True)
        self.modules = [
            mc_module,
            mr_module,
            mx_module,
            imu_module
        ]
        self.helper_executor(s)
        self.helper_timing(mc_module.execution_log, 0.02, 0.05)
        self.helper_timing(imu_module.execution_log, 0.01, 0.05)
        self.helper_timing(mr_module.execution_log, 0.01, 5.05)
        self.helper_timing(mx_module.execution_log, 0.01, 0.15)



if __name__ == '__main__':
    unittest.main()
