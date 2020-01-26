'''
Basic test for controlling motor speed with pwm.
'''

from gpiozero import Motor

'''
def setup():
    motor = Motor(23,24)
    return motor

if __name__ == '__main__':
    motor = setup()
    motor.forward()
    while True:
        pass
'''

#motor = Motor(17, 18)
#motor.forward()
from time import sleep

motor = Motor(forward=17, backward=18)

speed_max = 0.5
speed = 0.1
delta = 0.0001
while True:
    while speed < speed_max:
        motor.forward(speed=speed)
        speed += delta
        print(speed)
        sleep(0.005)
    while speed > 0.1:
        motor.forward(speed=speed)
        speed -= delta
        print(speed)
        sleep(0.005)

