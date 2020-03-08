import asyncio

import modules.state_printer as state_printer
import state

async def add_module(module):
    await module.run()

async def main():
    # Initialize state
    s = state.State()
    # Configure modules.
    reporter = state_printer.StatePrinter(s)

    await asyncio.gather(
        add_module(reporter)
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    
