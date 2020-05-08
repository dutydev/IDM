import os
import time
import sys
import string

from random import choice


class Logger:
    def __getattr__(self, item):
        if item in ["remove", "add", "level"]:
            return lambda *args, **kwargs: None
        return Logger()

    def __call__(self, message: str, *args, **kwargs):
        t = time.strftime("%m-%d %H:%M:%S", time.localtime())
        sys.stdout.write(
            "\n[IDM] " + message.format(*args, **kwargs) + " [TIME {}]".format(t)
        )


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        _rargs = list(args)
        for i in range(0, len(_rargs)):
            if type(_rargs[i]) is dict:
                for key in _rargs[i].keys():
                    if type(_rargs[i][key]) is dict:
                        _rargs[i][key] = DotDict(_rargs[i][key])

        for key in kwargs.keys():
            if type(kwargs[key]) is dict:
                kwargs[key] = DotDict(kwargs[key])

        super().__init__(*tuple(_rargs), **kwargs)

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def chunks(x, y):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(x), y):
        yield x[i:i + y]


def get_params(obj: dict) -> dict:
    return {
        k: v for k, v in obj.items()
        if k != "self" and not k.startswith("_") and v is not None
    }


def folder_checkup(path, create: bool = True):
    path = os.path.abspath(path)
    if not os.path.exists(path) and create:
        os.mkdir(path)
    return path


def generate_string(length: int = 15) -> str:
    mixin = string.ascii_lowercase + string.digits
    return ''.join(choice(mixin) for _ in range(length))


def sub_string(text: str) -> str:
    split = text.split()[0]
    return (text.replace(split, "")).strip()
