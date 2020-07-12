import importlib

def interface_provider(config):
    mod = importlib.import_module(config["python_module"])
    cls = getattr(mod, config["class"])
    obj = cls(config)
    return obj.get_interface()
