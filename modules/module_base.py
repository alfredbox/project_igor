import asyncio
import time

class ModuleBase:
    def __init__(self, state, cadence=None, logging=False):
        self.state = state
        self.cadence = cadence
        self.logging = logging
        self.execution_log = []

    def set_cadence(self, cadence):
        self.cadence = cadence

    def step(self):
        pass

    async def run(self):
        if self.logging:
            await self.run_and_log()
        else:
            await self.run_main()
            
    async def run_main(self):
        while True:
            await asyncio.sleep(self.cadence)
            self.step()

    async def run_and_log(self):
        while True:
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
