import asyncio
from gpiozero import DigitalInputDevice
import time

PORT_GREEN = 12
SBRD_GREEN = 13
PORT_WHITE = 5
SBRD_WHITE = 6

class MotorEncoderPair:
    def __init__(self, pin_a, pin_b, motor_state):
        self.encoder_a = MotorEncoder(pin_a, motor_state.encoder_a)
        self.encoder_b = MotorEncoder(pin_b, motor_state.encoder_b)
        self.encoder_a.set_twin_encoder(self.encoder_b)
        self.encoder_b.set_twin_encoder(self.encoder_a)


class MotorEncoder:
    def __init__(self, pin, encoder_state, main=True):
        self.encoder = DigitalInputDevice(pin)
        self.activation_history = encoder_state.activation_history
        self.direction_history = encoder_state.direction_history

        self.encoder.when_activated = self.on_detection

        self.twin_encoder = None;

    def set_twin_encoder(self, twin):
        self.twin_encoder = twin
            
    def on_detection(self):
        assert self.twin_encoder is not None, "Twin encoder has not been set."
        self.direction_history.append(self.twin_encoder.get_value())
        self.activation_history.append(time.time())

    def get_value(self):
        return self.encoder.value


class MotorReadModule:
    def __init__(self, state):
        self.state = state

    async def run(self):
        _ = MotorEncoderPair(
                PORT_GREEN, 
                PORT_WHITE, 
                self.state.drive_state.port_motor)
        _ = MotorEncoderPair(
                SBRD_GREEN, 
                SBRD_WHITE, 
                self.state.drive_state.sbrd_motor)
        while True:
            await asyncio.sleep(5) 
