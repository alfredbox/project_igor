import subprocess
import time

from libs.logger_setup import get_logger
from modules.module_base import ModuleBase

GET_THROTTLED_CMD = 'vcgencmd get_throttled'
MESSAGES = {
    0: 'Please recharge your battery',
    1: 'ARM frequency capped',
    2: 'Currently throttled',
    3: 'Soft temperature limit active',
    16: 'Under-voltage has occurred since last reboot.',
    17: 'Throttling has occurred since last reboot.',
    18: 'ARM frequency capped has occurred since last reboot.',
    19: 'Soft temperature limit has occurred'
}

logger = get_logger() 

class LowPower(Exception):
    pass

class PowerMonitorModule(ModuleBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 1
        super().__init__(state, cadence=DEFAULT_CADENCE_S)

    def step(self):
        throttled_output = subprocess.getoutput(GET_THROTTLED_CMD)
        throttled_output.strip()
        throttled_binary = bin(int(throttled_output.split('=')[1], 0))
        for position, message in MESSAGES.items():
            # Check for the binary digits to be "on" for each warning message
            if len(throttled_binary) > position and throttled_binary[0 - position - 1] == '1':
                if position == 0:
                    logger.error(message)
                    raise LowPower(message)
                else:
                    logger.warning(message)
