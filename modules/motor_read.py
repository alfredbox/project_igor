import asyncio
from gpiozero import DigitalInputDevice
import time


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
                12, 
                self.state.drive_state.port_motor.encoder_a.activation_history)
        # TODO set other three encoders.
        while True:
            await asyncio.sleep(5)

    


