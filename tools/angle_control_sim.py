import logging
import math
import time

import libs.logger_setup as logger_setup
from modules.imu_read import ImuReadModule
from modules.motor_controller import MotorControlModule
import state

logger_setup.setup(sim=True)
logger = logger_setup.get_logger()


class SimulatedMotorController:
    def __init__(self):
        self.throttle = 0.

class SimulatedMotorDriver:
    def __init__(self):
        self.motor3 = SimulatedMotorController()
        self.motor4 = SimulatedMotorController()

class SimulatedIMU:
    def __init__(self, angle_0, policy):
        self.angle = angle_0
        self.angle_0 = angle_0
        self.policy = policy
        self.euler = (0., self.angle, 0.)

    def update(self, elapsed):
        self.angle = self.policy(self.angle_0, elapsed)
        self.euler = (0., self.angle, 0.)


# Angle update policies
def constant(angle_0, elapsed):
    return angle_0

def linear2(angle_0, elapsed):
    return angle_0 + 2*elapsed

def sin2(angle_0, elapsed):
    return math.sin(elapsed*2)*angle_0
#######################


class MotorImuSimulation:
    def __init__(self, pid_coeffs, angle_0, policy, dt):
        self.state = state.State()
        self.mc = MotorControlModule(
            self.state, 
            simulated_motor_driver=SimulatedMotorDriver())
        Kp, Ki, Kd = coeffs
        self.mc.reset_pid(Kp, Ki, Kd)
        self.imu = ImuReadModule(
            self.state,
            simulated_imu=SimulatedIMU(angle_0, policy))
        self.dt = dt
                
    def sim_forward_for(self, secs): 
        starting = time.monotonic()
        elapsed = 0
        while (elapsed < secs):
            self.mc.step()
            self.imu.sensor.update(elapsed)
            self.imu.step()
            time.sleep(self.dt)
            t = time.monotonic()
            elapsed = t - starting 
               

if __name__ == "__main__":
    #kp 0.05 - 0.08
    #ki 0.01 - 0.2
    #kd 0.01 - 0.1
    coeffs = (0.0, 0., 0.08)
    sim = MotorImuSimulation(coeffs, -10., constant, 0.006)
    sim.sim_forward_for(3.)

