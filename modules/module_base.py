import asyncio

class ModuleBase:
    def __init__(self, state, cadence=None):
        self.state = state
        self.cadence = cadence

    def set_cadence(self, cadence):
        self.cadence = cadence

    def step(self):
        pass

    async def run(self):
        while True:
            await asyncio.sleep(self.cadence)
            self.step()

    def cleanup(self):
        pass
