import asyncio
import unittest
import time

import executor
import libs.logger_setup as logger_setup
import modules.power_monitor as power_monitor
import state
from testing.helpers import Terminator

class TestPowerMonitorModule(unittest.TestCase):
    def setUp(self):
        self.modules = []
    
    def helper_executor(self, state):
        terminator = Terminator(state, term_after_s=15)
        self.modules.append(terminator)
        executor.execute(self.modules)

    def test_power_monitor(self):
        s = state.State()
        mod = power_monitor.PowerMonitorModule(s) 
        self.modules.append(mod)
        self.helper_executor(s)

if __name__ == '__main__':
    logger_setup.setup()
    unittest.main()
