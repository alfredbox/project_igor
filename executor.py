import argparse
import asyncio
import importlib
import json

import libs.logger_setup as logger_setup
import modules.imu_read as imu_read
import modules.motor_read as motor_read
import modules.motor_compute as motor_compute
import modules.motor_controller as motor_controller
import modules.power_monitor as power_monitor
import modules.state_printer as state_printer

# Logging
logger_setup.setup()
logger = logger_setup.get_logger()

def assemble_modules(modules_cfg):
    # Initialize state
    state = importlib.import_module(modules_cfg["shared_state"])
    s = state.State()
    # Configure modules.
    modules = []
    for module_cfg in modules_cfg["modules"]:
        m = importlib.import_module(module_cfg["python_module"])
        mc = getattr(m, module_cfg["class"])
        modules.append(mc(s))

    return modules

async def add_module(module):
    await module.run()

def cleanup(modules):
    for m in modules:
        m.cleanup()

def execute(modules):
    async def execute_main():
        nonlocal modules 
        tasks = [add_module(m) for m in modules]
        await asyncio.gather(
            *tasks
        )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(execute_main())
        loop.close()
    finally:
        cleanup(modules)

def main(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    logger.info('Activating {}'.format(config["executor_name"])) 
    modules = assemble_modules(config["modules_config"])
    execute(modules)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="General executor.")
    parser.add_argument(
        "config_path", 
        type=str, 
        help="Path to the executor configuration")
    args = parser.parse_args()

    main(args.config_path)
