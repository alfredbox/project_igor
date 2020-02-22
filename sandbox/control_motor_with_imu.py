import time
from adafruit_motorkit import MotorKit
import adafruit_bno055

from busio import I2C
from board import SDA, SCL

i2c = I2C(SCL, SDA) 

sensor = adafruit_bno055.BNO055(i2c)

kit = MotorKit()

signal = 0
while True:
    p_signal = sensor.gravity[1]
    if p_signal is not None:
        signal = min(p_signal*0.1,1)
        signal = max(signal, -1)
        print(signal)
    kit.motor3.throttle = signal
    #time.sleep(0.01)
