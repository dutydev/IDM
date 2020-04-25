from ..framework.handler import Handler, MessageHandler
from ..objects.methods import Method
from ..utils import logger

from typing import List, Callable, Union
from inspect import iscoroutinefunction

Text = Union[str, List[str]]


class Event:
    def __init__(self):
        self.handler: List[Handler] = list()
        self.message_handler: List[MessageHandler] = list()

    def concatenate(self, handler: "Event"):
        """
        Concatenate handlers from another handler.
        """
        self.handler += handler.handler
        self.message_handler += handler.message_handler
        logger.debug(
            "Current handler was concatenated with {handler}",
            handler=handler.__class__.__name__
        )

    def add_handler(self, func: Callable, method: Method):
        if not iscoroutinefunction(func):
            raise TypeError("Handler has to be coroutine function.")
        handler = Handler(func, method)
        self.handler.append(handler)

    def add_message_handler(
        self,
        func: Callable,
        method: Method,
        text: Text,
        lower: bool = True
    ):
        if not iscoroutinefunction(func):
            raise TypeError("Handler has to be coroutine function.")
        message_handler = MessageHandler(func, method, text, lower)
        self.message_handler.append(message_handler)

    def event(self, method: Method):
        def decorator(func):
            self.add_handler(func, method)
            return func
        return decorator

    def message_event(
        self,
        method: Method,
        text: Text,
        lower: bool = False
    ):
        def decorator(func):
            if method.value not in ("sendSignal", "sendMySignal"):
                raise ValueError("Invalid method")
            self.add_message_handler(func, method, text, lower)
            return func
        return decorator



