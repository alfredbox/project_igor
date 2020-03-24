import asyncio
from datetime import datetime, timezone
import os

class StatePrinter:
    def __init__(self, state, cadence=1):
        self.state=state
        self.set_cadence(cadence)

    def set_cadence(self, cadence):
        self.cadence = cadence

    def motor_msg(self, side, motor): 
        msg = (
            '{side} motor:\n'
            '\tThrottle: {throttle}\n'
            '\tSpeed: {rpm:.1f} rpm\n'
            '\tDirection: {direction}'
        )
        direction = 'forward' if motor.direction else 'backward'
        return msg.format(
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

    async def run(self):
        while True:
            await asyncio.sleep(self.cadence)
            os.system('clear')
            self.print_state()

    def cleanup(self):
        print('Exiting..')
