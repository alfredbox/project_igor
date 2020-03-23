from adafruit_motorkit import MotorKit

import asyncio
import state

class Motor:
    def __init__(self, motor_state, controller):
        self.controller = controller
        self.motor_state = motor_state

    def set_throttle(self, val):
        assert (val <= 1. and val >= -1.), (
            "Throttle must be between -1.0 and 1.0")
        self.controller.throttle = val
        self.motor_state.throttle = val
        
class MotorModule:
    def __init__(self, state):
        kit = MotorKit()
        self.drive_state = state.drive_state
        # Port Motor
        self.port_motor = Motor(self.drive_state.port_motor, kit.motor3)
        # Starboard Motor
        self.sbrd_motor = Motor(self.drive_state.sbrd_motor, kit.motor4)

    def control_policy(self):
        # TODO make less trivial
        self.port_motor.set_throttle(0.5)
        self.sbrd_motor.set_throttle(0.5)

    async def run(self):
        while True:
            await asyncio.sleep(0.1)
            self.control_policy()
