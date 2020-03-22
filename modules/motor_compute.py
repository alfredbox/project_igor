import asyncio

GEARING = 20.
ENCODERMULT = 12.
QUEUE_LEN = 4

class MotorEncoder:
    def __init__(self, activation_history):
        self.activation_history = activation_history

    def get_history(self):
        return self.activation_history

    def ready(self):
        return len(self.activation_history) == self.activation_history.maxlen
    
    def latest_time(self):
        return self.activation_history[-1] if self.ready() else None
    
    def instant_time_d(self):
        return (self.activation_history[-1] - self.activation_history[-2] 
                if self.ready() else None)

    def averaged_time_d(self):
        if not self.ready():
            return None
        d1 = self.activation_history[-1] - self.activation_history[-2]
        d2 = self.activation_history[-2] - self.activation_history[-3]
        return (d1 + d2) / 2.0

    def rpm(self):
        return (60. / (self.instant_time_d() * GEARING * ENCODERMULT) 
                if self.ready() else None)

class Motor:
    def __init__(self, motor_state):
        self.motor_state = motor_state
        self.encoder_a = MotorEncoder(motor_state.encoder_a.activation_history)
        self.encoder_b = MotorEncoder(motor_state.encoder_b.activation_history)

    def propagate_state(self):
        if self.encoder_a.ready() and self.encoder_b.ready():
            self.motor_state.direction = (
                self.encoder_a.latest_time() > 
                self.encoder_b.latest_time())
            self.motor_state.rpm = (self.encoder_a.rpm() + self.encoder_b.rpm()) / 2.0

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

