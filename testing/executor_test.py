import asyncio
import unittest
import time

import executor
from modules.module_base import ModuleBase
import state

class TaskState:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

class State(state.State):
    def __init__(self):
        super().__init__()
        self.task_a = TaskState()
        self.task_b = TaskState()

class WaitAndSetState(ModuleBase, unittest.TestCase):
    def __init__(self, state, config=""):
        super().__init__(state, config=config, cadence=1)
        if self.config["task_id"] == 'a':
            self.task_state = state.task_a
        elif self.config["task_id"] == 'b':
            self.task_state = state.task_b

    def step(self):
        if not self.task_state.start_time:
            self.task_state.start_time = time.time()
        elif not self.task_state.end_time:
            self.task_state.end_time = time.time()
        elif self.state.task_a.end_time and self.state.task_b.end_time:
            self.state.execution_control.termination_requested = True

    def cleanup(self):
        tc = unittest.TestCase()
        tc.assertGreater(self.state.task_a.start_time, 0)
        tc.assertGreater(self.state.task_b.start_time, 0)
        tc.assertAlmostEqual(
            self.state.task_a.start_time,
            self.state.task_b.start_time,
            places=3)
        tc.assertGreaterEqual(
            (self.state.task_a.end_time - self.state.task_a.start_time),
            1)
        tc.assertGreaterEqual(
            (self.state.task_b.end_time - self.state.task_b.start_time), 
            1)
        tc.assertAlmostEqual(
            self.state.task_a.end_time, 
            self.state.task_b.end_time, 
            places=3)

class TestExecutor(unittest.TestCase): 

    def test_async_running(self):
        executor.main("testing/config/test_exec.json")


if __name__ == '__main__':
    unittest.main()
