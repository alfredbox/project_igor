import asyncio
import unittest
import time

import executor
import state
from testing.helpers import TestMotorControllerBasic

class TestTimingOneModule(unittest.TestCase):
    
    def helper_executor(self, module_under_test):
        s = state.State()
        modules = [module_under_test]
        executor.execute(modules)
        self.assertTrue(module_under_test.execution_log)

    def helper_timing(self, log, duration_tol, cadence_tol):
        last_time = None
        for ts in log:
            self.assertLess(ts['ran_for_s'], duration_tol)
            if last_time is not None:
                cadence = ts['ran_at_s'] - last_time
                self.assertLess(cadence, cadence_tol)
            last_time = ts['ran_at_s']

    def test_module_timing(self):
        s = state.State()
        mc_module = TestMotorControllerBasic(s, logging=True)
        self.helper_executor(mc_module)
        self.helper_timing(mc_module.execution_log, 0.01, 0.05)

if __name__ == '__main__':
    unittest.main()
