'''
A simple program to read in the state of a motor encoder
pin and compute and print the speed in RPM.
'''
from collections import deque
from gpiozero import DigitalInputDevice
import time
from signal import pause

GEARING = 20.
ENCODERMULT = 12.
QUEUE_LEN = 4

class MotorEncoder:
    def __init__(self, pin):
        self.encoder = DigitalInputDevice(pin)
        self.activation_history = deque(maxlen=QUEUE_LEN) 
        self.encoder.when_activated = self.on_detection

    def on_detection(self):
        self.activation_history.append(time.time())
        print(self.rpm())

    def get_history(self):
        return self.activation_history

    def instant_time_d(self):
        return self.activation_history[-1] - self.activation_history[-2]

    def averaged_time_d(self):
        d1 = self.activation_history[-1] - self.activation_history[-2]
        d2 = self.activation_history[-2] - self.activation_history[-3]
        return (d1 + d2) / 2.0

    def rpm(self):
        if len(self.activation_history) != QUEUE_LEN:
            return None
        return 60. / (self.instant_time_d() * GEARING * ENCODERMULT)
        


def setup():
    encoder_a = MotorEncoder(12)
    #    encoder_a.wait_for_active()
    #    print('ON!')
    #    encoder_a.wait_for_inactive()
    #    print('OFF!')
    #encoder_a.when_activated = on_change
    #encoder_a.when_deactivated = on_change
    pause()
    while True:
        print("spinning")
        time.sleep(1)

if __name__ == "__main__":
    print('Testing motor speed')
    setup()

    #pause()
