import asyncio
import time

import executor
import libs.logger_setup as logger_setup
import modules.remote_control as remote_control
import state
from testing.helpers import Terminator

class TestRemoteControlModule:
    def __init__(self):
        self.modules = []
    
    def helper_executor(self, state):
        terminator = Terminator(state, term_after_s=15)
        self.modules.append(terminator)
        executor.execute(self.modules)

    def setup_remote_control_server(self):
        s = state.State()
        mod = remote_control.RemoteControlModule(s)
        self.modules.append(mod)
        self.helper_executor(s)

if __name__ == '__main__':
    logger_setup.setup()
    test = TestRemoteControlModule()
    test.setup_remote_control_server()
