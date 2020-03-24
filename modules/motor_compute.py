import asyncio
from statistics import mean
import time

GEARING = 20.
ENCODERMULT = 12.

class MotorEncoder:
    def __init__(self, encoder_state):
        self.activation_history = encoder_state.activation_history
        self.direction_history = encoder_state.direction_history
        self.last_filtered_time = 1

    def ready(self):
        return (len(self.activation_history) 
                    == self.activation_history.maxlen and 
                len(self.direction_history) 
                    == self.direction_history.maxlen)
    
    def latest_time(self):
        return self.activation_history[-1] if self.ready() else None
    
    def latest_direction(self):
        return self.direction_history[-1]  if self.ready() else None
    
    def instant_time_d(self):
        return (self.activation_history[-1] - self.activation_history[-2] 
                if self.ready() else None)

    def averaged_time_d(self):
        if not self.ready():
            return None
        d1 = self.activation_history[-1] - self.activation_history[-2]
        d2 = self.activation_history[-2] - self.activation_history[-3]
        return (d1 + d2) / 2.0

    def low_pass_filtered_time_d(self):
        last = None
        deltas = []
        for t in self.activation_history:
            if last is not None:
                deltas.append(t-last)
            last = t

        contemporary_delta = time.time() - self.activation_history[-1]
        if contemporary_delta > 2*mean(deltas):
            alpha = 0.5
            self.last_filtered_time = (self.last_filtered_time*(1.0-alpha)
                                       + alpha*contemporary_delta)
        else:
            alpha = 0.1
            for d in deltas:
                self.last_filtered_time = (self.last_filtered_time*(1.0-alpha)
                                           + alpha*d)
        return self.last_filtered_time

    def averaged_direction(self):
        direction_sum = sum(self.direction_history)
        return direction_sum >= len(self.direction_history)*0.5

    def rpm(self):
        return (60. / (self.low_pass_filtered_time_d() * GEARING * ENCODERMULT) 
                if self.ready() else None)


class Motor:
    def __init__(self, motor_state):
        self.motor_state = motor_state
        self.encoder_a = MotorEncoder(motor_state.encoder_a)
        self.encoder_b = MotorEncoder(motor_state.encoder_b)

    def propagate_state(self):
        if self.encoder_a.ready() and self.encoder_b.ready():
            # Note using throttle sign to determine direction as
            # quad encoder signal is noisy.
            self.motor_state.direction = self.motor_state.throttle < 0
            self.motor_state.rpm = (self.encoder_a.rpm() 
                                    + self.encoder_b.rpm()) / 2.0


class MotorCompute:
    def __init__(self, state):
        self.motors = [
            Motor(state.drive_state.port_motor),
            Motor(state.drive_state.sbrd_motor)
        ]

    async def run(self):
        while True:
            await asyncio.sleep(0.1)
            for m in self.motors:
                m.propagate_state()

