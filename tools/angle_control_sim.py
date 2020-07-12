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

class MotorImuSimulation:
    def __init__(self, pid_coeffs, imu_config, motor_controller_config, dt):
        self.state = state.State()
        self.mc = MotorControlModule(
            self.state, 
            config=motor_controller_config)
        Kp, Ki, Kd = coeffs
        self.mc.angle_control.update_coeffs(Kp, Ki, Kd)
        self.imu = ImuReadModule(
            self.state,
            config=imu_config)
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
    imu_config = "testing/config/modules/sim_imu_const_config.json"
    motor_controller_config = ("testing/config/modules/"
                               "sim_motor_controller_config_00.json")
    sim = MotorImuSimulation(coeffs,  
                             imu_config, 
                             motor_controller_config, 
                             0.006)
    sim.sim_forward_for(3.)

