import asyncio
from gpiozero import DigitalInputDevice
import time

PORT_GREEN = 12
SBRD_GREEN = 13
PORT_WHITE = 5
SBRD_WHITE = 6

class MotorEncoder:
    def __init__(self, pin, encoder_queue):
        self.encoder = DigitalInputDevice(pin)
        self.activation_history = encoder_queue
        self.encoder.when_activated = self.on_detection

    def on_detection(self):
        self.activation_history.append(time.time())

    def get_history(self):
        return self.activation_history


class MotorReadModule:
    def __init__(self, state):
        self.state = state

    async def run(self):
        _ = MotorEncoder(
                PORT_GREEN, 
                self.state.drive_state.port_motor.encoder_a.activation_history)
        _ = MotorEncoder(
                PORT_WHITE, 
                self.state.drive_state.port_motor.encoder_b.activation_history)
        _ = MotorEncoder(
                SBRD_GREEN, 
                self.state.drive_state.sbrd_motor.encoder_a.activation_history)
        _ = MotorEncoder(
                SBRD_WHITE, 
                self.state.drive_state.sbrd_motor.encoder_b.activation_history)
        # TODO set other three encoders.
        while True:
            await asyncio.sleep(5)

    


