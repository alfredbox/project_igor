import time
import adafruit_bno055

from busio import I2C
from board import SDA, SCL

i2c = I2C(SCL, SDA)


sensor = adafruit_bno055.BNO055(i2c)

while True:
    #print("Euler {}".format(sensor.euler))
    signal = sensor.gravity
    if None not in signal:
        print(signal)
        time.sleep(0.1)
