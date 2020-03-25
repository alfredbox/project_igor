from datetime import datetime, timezone
import os

from modules.module_base import ModuleBase

class StatePrintModule(ModuleBase):
    def __init__(self, state, debug=False):
        self.debug = debug
        DEFAULT_CADENCE_S = 1
        super().__init__(state, cadence=DEFAULT_CADENCE_S)

    def motor_msg(self, side, motor): 
        msg = (
            '{side} motor:\n'
            '\tThrottle: {throttle}\n'
            '\tSpeed: {rpm:.1f} rpm\n'
            '\tDirection: {direction}'
        )
        direction = 'forward' if motor.direction else 'backward'
        msg = msg.format(
            side=side,
            throttle=motor.throttle,
            rpm=motor.rpm,
            direction=direction,
        )
    
    def print_state(self):
        drive_state = self.state.drive_state
        drive_msg = (
            '**Drive State:\n'
            '{port_state}\n'
            '{sbrd_state}'
        ).format(
            port_state=self.motor_msg('Port', drive_state.port_motor),
            sbrd_state=self.motor_msg('Starboard', drive_state.sbrd_motor)
        )
        ts = datetime.now(timezone.utc)
        tmsg = ts.astimezone().strftime('%a %b %d %H:%M:%S %Y %z')
        print('\nData at {}'.format(tmsg))
        print(drive_msg)
        print('\n')

    def step(self):
        os.system.clear()
        self.print_state()

    def cleanup(self):
        print('Exiting..')
