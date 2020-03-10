import asyncio
import unittest
import signal
import time

import executor
from testing.helpers import TaskState, SimpleState


class Transmitter:
    def __init__(self, task_state):
        self.task_state = task_state

    async def run(self):
        self.task_state.start_time = time.time()
        signal.alarm(1)
        await asyncio.sleep(0.5)
        self.task_state.end_time = time.time()

    
class Reciever:
    def __init__(self, task_state):
        self.task_state = task_state
    
    def handler(self, signm, frame):
        self.task_state.end_time = time.time()

    async def run(self):
        self.task_state.start_time = time.time()     
        signal.signal(signal.SIGALRM, self.handler)
        await asyncio.sleep(1.1)
   

def helper_assemble_modules(state):
    tx = Transmitter(state.task_a)
    rx = Reciever(state.task_b)
    return [tx, rx]


class TestSignalling(unittest.TestCase):
    def test_async_signals(self):
        state = SimpleState()
        modules = helper_assemble_modules(state)
        executor.execute(modules)

        self.assertGreater(state.task_a.start_time, 0)
        self.assertGreater(state.task_b.start_time, 0)
        self.assertAlmostEqual(state.task_a.start_time, 
                               state.task_b.start_time, 
                               places=3)
        self.assertGreaterEqual(
            (state.task_b.end_time - state.task_b.start_time),
            1)
        task_a_elapsed = state.task_a.end_time - state.task_a.start_time
        self.assertGreaterEqual(task_a_elapsed, 0.5)
        self.assertLess(task_a_elapsed, 1.0)


if __name__ == '__main__':
    unittest.main()
