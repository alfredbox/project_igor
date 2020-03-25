import unittest
import time

import modules.motor_compute as motor_compute
import state

from testing.helpers import TaskState, SimpleState


class TestEncoderCompute(unittest.TestCase):
    def setUp(self):
        self.state = state.State()
        self.encoder_state = self.state.drive_state.port_motor.encoder_a
        self.encoder = motor_compute.EncoderCompute(self.encoder_state)

    def helper_populate_encoder_state(self): 
        n = self.encoder.activation_history.maxlen
        times = [0.1*t for t in range(n)]
        for t in times:
            self.encoder_state.activation_history.append(t)
            self.encoder_state.direction_history.append(1)
        
    def test_initialization(self):
        self.assertEqual(len(self.encoder.activation_history), 0)
        self.assertEqual(len(self.encoder.direction_history), 0)

        self.assertIsNone(self.encoder.latest_time())
        self.assertIsNone(self.encoder.latest_direction())
        self.assertIsNone(self.encoder.instant_time_d())
        self.assertIsNone(self.encoder.averaged_time_d())
        self.assertIsNone(self.encoder.low_pass_filtered_time_d())
        self.assertIsNone(self.encoder.averaged_direction())
        self.assertIsNone(self.encoder.rpm())

        self.assertFalse(self.encoder.ready())

    def test_fetch_latest(self):
        n = self.encoder.activation_history.maxlen
        times = [0.1*t for t in range(n)]
        for t in times:
            self.assertIsNone(self.encoder.latest_time())
            self.assertIsNone(self.encoder.latest_direction())
            self.encoder_state.activation_history.append(t)
            self.encoder_state.direction_history.append(1)
        self.assertEqual(times[-1], self.encoder.latest_time())
        self.assertEqual(1, self.encoder.latest_direction())

    def test_instant_time(self):
        self.helper_populate_encoder_state()
        self.assertAlmostEqual(0.1, self.encoder.instant_time_d())
    
    def test_average_time(self):
        self.helper_populate_encoder_state()
        self.assertAlmostEqual(0.1, self.encoder.averaged_time_d())
    
if __name__ == '__main__':
    unittest.main()
