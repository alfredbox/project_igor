import asyncio

import libs.logger_setup as logger_setup
import modules.imu_read as imu_read
import modules.motor_read as motor_read
import modules.motor_compute as motor_compute
import modules.motor_controller as motor_controller
import modules.state_printer as state_printer
import state

# Logging
logger_setup.setup()
logger = logger_setup.get_logger()

def assemble_modules():
    # Initialize state
    s = state.State()
    # Configure modules.
    modules = []
    # State printer
    #modules.append(state_printer.StatePrintModule(s))
    # Motor Encoders Reader
    modules.append(motor_read.MotorReadModule(s))
    # Motor State comptation
    modules.append(motor_compute.MotorComputeModule(s))
    # Motor Control
    modules.append(motor_controller.MotorControlModule(s))
    # Imu Reader    
    modules.append(imu_read.ImuReadModule(s))
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
    finally:
        cleanup(modules)


if __name__ == "__main__":
    logger.info('Activating Igor') 
    modules = assemble_modules()
    execute(modules)
