import os
import time
import sys
import string

from random import choice


class Logger:
    def __getattr__(self, item):
        if item in ("remove", "add", "level"):
            return lambda *args, **kwargs: None
        return Logger()

    def __call__(self, message: str, *args, **kwargs):
        t = time.strftime("%m-%d %H:%M:%S", time.localtime())
        try:
            # TODO: Придумать что-нибудь по лучше
            message = message.format(*args, **kwargs)
        except KeyError:
            pass
        sys.stdout.write(
            f"\n[IDM] {message} [TIME {t}]"
        )


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
