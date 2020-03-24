import asyncio

import modules.motor_read as motor_read
import modules.motor_compute as motor_compute
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
    # Motor Encoders Reader
    modules.append(motor_read.MotorReadModule(s))
    # Motor State comptation
    modules.append(motor_compute.MotorCompute(s))
    return modules

async def add_module(module):
    await module.run()

def cleanup(modules):
    for m in modules:
        m.cleanup()

def execute(modules):
    async def main():
        nonlocal modules 
        tasks = [add_module(m) for m in modules]
        await asyncio.gather(
            *tasks
        )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    except:
        cleanup(modules)

if __name__ == "__main__":
   modules = assemble_modules()
   execute(modules)
