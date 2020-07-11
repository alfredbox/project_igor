import argparse
import asyncio
import importlib
import json

import libs.logger_setup as logger_setup

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
        c = module_cfg["config"]
        modules.append(mc(s, config=c))

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
