from typing import TypeVar, Type
import contextvars

T = TypeVar("T")


class ContextInstanceMixin:
    """
    Author: https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/utils/mixins.py
    """

    def __init_subclass__(cls, **kwargs):
        cls.__context_instance = contextvars.ContextVar("instance_" + cls.__name__)
        return cls

    @staticmethod
    def get_params(params: dict) -> dict:
        return {
            k: v for k, v in params.items()
            if k != "self" and not k.startswith("_") and v is not None
        }

    @classmethod
    def get_current(cls: Type[T], no_error=True) -> T:
        if no_error:
            return cls.__context_instance.get(None)
        return cls.__context_instance.get()

    @classmethod
    def set_current(cls: Type[T], value: T):
        cls.__context_instance.set(value)