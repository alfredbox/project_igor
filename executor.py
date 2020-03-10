import asyncio

import modules.state_printer as state_printer
import state

def assemble_modules():
    # Initialize state
    s = state.State()
    # Configure modules.
    modules = []
    # Reporter module
    reporter = state_printer.StatePrinter(s)
    modules.append(reporter)
    return modules

async def add_module(module):
    await module.run()

def execute(modules):
    async def main():
        nonlocal modules 
        tasks = [add_module(m) for m in modules]
        await asyncio.gather(
            *tasks
        )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

if __name__ == "__main__":
   modules = assemble_modules()
   execute(modules)
