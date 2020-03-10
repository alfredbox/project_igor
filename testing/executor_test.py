import asyncio
import unittest
import time

import executor
from testing.helpers import TaskState, SimpleState


class WaitAndSetState:
    def __init__(self, task_state):
        self.task_state = task_state

    async def run(self):
        self.task_state.start_time = time.time()
        await asyncio.sleep(1)
        self.task_state.end_time = time.time()


def helper_assemble_modules(state):
    set_a = WaitAndSetState(state.task_a)
    set_b = WaitAndSetState(state.task_b)
    return [set_a, set_b]


class TestExecutor(unittest.TestCase):
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
