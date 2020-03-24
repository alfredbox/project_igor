import collections

QUEUE_LEN = 8

class EncoderState:
    def __init__(self):
        self.activation_history = collections.deque(maxlen=QUEUE_LEN)
        self.direction_history = collections.deque(maxlen=QUEUE_LEN) 

class MotorState:
    def __init__(self):
        self.direction = True # Forward
        self.rpm = 0
        self.throttle = 0
        # Raw state data
        self.encoder_a = EncoderState()
        self.encoder_b = EncoderState()

class DriveState:
    def __init__(self):
        self.port_motor = MotorState()
        self.sbrd_motor = MotorState()

class IMUState:
    def __init__(self):
        self.gravity = (0., 0., 0.)

class State:
    def __init__(self):
        self.imu_state = IMUState()
        self.drive_state = DriveState() 
