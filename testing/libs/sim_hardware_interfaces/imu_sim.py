import math

from libs.hardware_interface.base_interface import BaseInterface

class SimulatedImu:
    def __init__(self, angle_0, policy):
        self.angle = angle_0
        self.angle_0 = angle_0
        self.policy = policy
        self.euler = (0., self.angle, 0.)

    def update(self, elapsed):
        self.angle = self.policy(self.angle_0, elapsed)
        self.euler = (0., self.angle, 0.)


# angle update policies
def constant(angle_0, elapsed):
    return angle_0

def linear2(angle_0, elapsed):
    return angle_0 + 2*elapsed

def sin2(angle_0, elapsed):
    return math.sin(elapsed*2)*angle_0


class SimulatedImuInterface(BaseInterface):
    
    def get_interface(self):
        policy = eval(self.config["policy"])
        angle_0 = self.config["angle_0"]
        return SimulatedImu(angle_0, policy)
