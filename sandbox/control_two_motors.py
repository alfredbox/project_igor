import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

#kit.motor1.throttle = -1.0

count = 0
while True:
    if count < 10000:
        kit.motor1.throttle = 0
        kit.motor3.throttle = 0.5
    elif count < 20000:
        kit.motor3.throttle = 0
        kit.motor1.throttle = 0.5
    else:
        count = 0
    count += 1
    print(count)
