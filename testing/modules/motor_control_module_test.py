import unittest

import modules.motor_controller as mc
import state

class DummyController:
    def __init__(self):
        self.throttle = 0


class TestMotorController(unittest.TestCase):
    def setUp(self):
        self.state = state.State()
        self.port_motor_state = self.state.drive_state.port_motor
        self.port_controller = DummyController()

    def test_deadband(self):
        motor_control = mc.MotorControl(
            self.port_motor_state, self.port_controller)
        null = 0
        self.assertEqual(motor_control._deadband_rm(null), null)
        uno = 1
        self.assertEqual(motor_control._deadband_rm(uno), uno)
        muno = -1
        self.assertEqual(motor_control._deadband_rm(muno), muno)
        tiny = 0.0001
        self.assertGreater(motor_control._deadband_rm(tiny), 0.3)
        mtiny = -0.0001
        self.assertLess(motor_control._deadband_rm(mtiny), -0.3)

    def test_throttle_set(self):
        motor_control = mc.MotorControl(
            self.port_motor_state, self.port_controller)
        null = 0
        motor_control.set_throttle(null)
        self.assertEqual(self.port_motor_state.throttle, null)
        self.assertEqual(self.port_controller.throttle, null)
        uno = 1
        motor_control.set_throttle(uno)
        self.assertEqual(self.port_motor_state.throttle, uno)
        self.assertEqual(self.port_controller.throttle, uno)
        muno = -1
        motor_control.set_throttle(muno)
        self.assertEqual(self.port_motor_state.throttle, muno)
        self.assertEqual(self.port_controller.throttle, muno)
        tiny = 0.0001
        motor_control.set_throttle(tiny)
        self.assertEqual(self.port_motor_state.throttle, tiny)
        self.assertGreater(self.port_controller.throttle, 0.3)
        mtiny = -0.0001
        motor_control.set_throttle(mtiny)
        self.assertEqual(self.port_motor_state.throttle, mtiny)
        self.assertLess(self.port_controller.throttle, -0.3)

        
if __name__ == "__main__":
    unittest.main()
