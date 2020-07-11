import asyncio
import json
import time

class ModuleBase:
    def __init__(self, state, config="", cadence=None):
        self.state = state
        if config:
            with open(config, 'r') as f:
                self.config = json.load(f)
        self.cadence = cadence
        self.logging = False
        self.execution_log = []

    def set_cadence(self, cadence):
        self.cadence = cadence

    def set_logging(self, should_log):
        self.logging = should_log

    def step(self):
        pass

    async def run(self):
        if self.logging:
            await self.run_and_log()
        else:
            await self.run_main()
            
    async def run_main(self):
        while not self.state.execution_control.termination_requested:
            await asyncio.sleep(self.cadence)
            self.step()

    async def run_and_log(self):
        while not self.state.execution_control.termination_requested:
            await asyncio.sleep(self.cadence)
            commence = time.time()
            self.step()
            finish = time.time()
            self.execution_log.append({
                "ran_at_s": commence,
                "ran_for_s": finish - commence
            })

    def cleanup(self):
        pass
