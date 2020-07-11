import unittest
import signal
import time

import executor
from modules.module_base import ModuleBase
from testing.executor_test import TaskState, State


class Transmitter(ModuleBase):
    def __init__(self, state, config=""):
        super().__init__(state, cadence=0.5)
        self.task_state = self.state.task_a

    def step(self):
        if not self.task_state.start_time:
            self.task_state.start_time = time.time()
        elif not self.task_state.end_time:
            signal.alarm(1)
            self.task_state.end_time = time.time()
        elif self.state.task_a.end_time and self.state.task_b.end_time:
            self.state.execution_control.termination_requested = True


class Reciever(ModuleBase):
    def __init__(self, state, config=""):
        super().__init__(state, cadence=1.1)
        self.task_state = self.state.task_b

    def handler(self, signm, frame):
        self.task_state.end_time = time.time()

    def step(self):
        if not self.task_state.start_time:
            self.task_state.start_time = time.time()
            signal.signal(signal.SIGALRM, self.handler)
        elif self.state.task_a.end_time and self.state.task_b.end_time:
            self.state.execution_control.termination_requested = True 

    def cleanup(self):
        tc = unittest.TestCase()
        tc.assertGreater(self.state.task_a.start_time, 0)
        tc.assertGreater(self.state.task_b.start_time, 0)
        tc.assertAlmostEqual(0.6, 
                             abs(self.state.task_a.start_time - 
                                 self.state.task_b.start_time),
                             places=3)
        tc.assertGreaterEqual(
            (self.state.task_b.end_time - self.state.task_b.start_time),
            0.6)
        task_a_elapsed = (self.state.task_a.end_time - 
                          self.state.task_a.start_time)
        tc.assertGreaterEqual(task_a_elapsed, 0.5)
        tc.assertLess(task_a_elapsed, 1.0)


def helper_assemble_modules(state):
    tx = Transmitter(state)
    rx = Reciever(state)
    return [tx, rx]


class TestSignalling(unittest.TestCase):
    #@unittest.SkipTest
    def test_async_signals(self):
        executor.main("testing/config/test_signal_exec.json")


if __name__ == '__main__':
    unittest.main()
