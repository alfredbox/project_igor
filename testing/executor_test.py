import asyncio
import unittest
import time

import executor
from modules.module_base import ModuleBase
from testing.helpers import TaskState, SimpleState


class WaitAndSetState(ModuleBase):
    def __init__(self, state, task):
        super().__init__(state, cadence=1)
        if task == 'a':
            self.task_state = state.task_a
        elif task == 'b':
            self.task_state = state.task_b

    def step(self):
        if not self.task_state.start_time:
            self.task_state.start_time = time.time()
        elif not self.task_state.end_time:
            self.task_state.end_time = time.time()
        elif self.state.task_a.end_time and self.state.task_b.end_time:
            self.state.execution_control.termination_requested = True


def helper_assemble_modules(state):
    set_a = WaitAndSetState(state, 'a')
    set_b = WaitAndSetState(state, 'b')
    return [set_a, set_b]


class TestExecutor(unittest.TestCase):
    @unittest.SkipTest
    def test_async_running(self):
        state = SimpleState()
        modules = helper_assemble_modules(state)
        executor.execute(modules)

        self.assertGreater(state.task_a.start_time, 0)
        self.assertGreater(state.task_b.start_time, 0)
        self.assertAlmostEqual(state.task_a.start_time, 
                               state.task_b.start_time, 
                               places=3)
        self.assertGreaterEqual(
            (state.task_a.end_time - state.task_a.start_time),
            1)
        self.assertGreaterEqual(
            (state.task_b.end_time - state.task_b.start_time), 
            1)
        self.assertAlmostEqual(state.task_a.end_time, 
                               state.task_b.end_time, 
                               places=3)


if __name__ == '__main__':
    unittest.main()
