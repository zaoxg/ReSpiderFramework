import importlib


def load_object(path):
    """
    Load an object given its absolute object path, and return it.
    """
    if not isinstance(path, str):
        if callable(path):
            return path
        else:
            raise TypeError("Unexpected argument type, expected string "
                            "or object, got: %s" % type(path))
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError(f"Error loading object '{path}': not a full path")

    module, name = path[:dot], path[dot + 1:]
    mod = importlib.import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        obj = importlib.import_module(path)
        # raise NameError(f"Module '{module}' doesn't define any object named '{name}'")

    return obj


def load_settings(module: str = None):
    """
    加载默认的配置文件
    :return:
    """
    settings = {}
    module = load_object(module or 'ReSpider.setting')
    for _, obj in module.__dict__.items():
        settings[_] = obj
    settings.pop('__name__')
    settings.pop('__doc__')
    settings.pop('__package__')
    settings.pop('__loader__')
    settings.pop('__spec__')
    settings.pop('__file__')
    settings.pop('__cached__')
    settings.pop('__builtins__')
    return settings
