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

    def add_handler(self, method: Method, func: Callable):
        if not iscoroutinefunction(func):
            raise TypeError("Handler has to be coroutine function.")
        handler = Handler(func, method)
        self.handler.append(handler)

    def add_message_handler(
        self,
        method: Method,
        func: Callable,
        text: Text,
        lower: bool = True
    ):
        if not iscoroutinefunction(func):
            raise TypeError("Handler has to be coroutine function.")
        message_handler = MessageHandler(func, method, text, lower)
        self.message_handler.append(message_handler)

    def ping(self):
        def decorator(func):
            self.add_handler(Method.PING, func)
            return func

        return decorator

    def subscribe_signals(self):
        def decorator(func):
            self.add_handler(Method.SUBSCRIBE_SIGNALS, func)
            return func

        return decorator

    def ban_expired(self):
        def decorator(func):
            self.add_handler(Method.BAN_EXPIRED, func)
            return func

        return decorator

    def add_user(self):
        def decorator(func):
            self.add_handler(Method.ADD_USER, func)
            return func

        return decorator

    def delete_messages(self):
        def decorator(func):
            self.add_handler(Method.DELETE_MESSAGES, func)
            return func

        return decorator

    def hire_api(self):
        def decorator(func):
            self.add_handler(Method.HIRE_API, func)
            return func

        return decorator

    def delete_messages_from_user(self):
        def decorator(func):
            self.add_handler(Method.DELETE_MESSAGES_FROM_USER, func)
            return func

        return decorator

    def print_bookmark(self):
        def decorator(func):
            self.add_handler(Method.PRINT_BOOKMARK, func)
            return func

        return decorator

    def forbidden_links(self):
        def decorator(func):
            self.add_handler(Method.FORBIDDEN_LINKS, func)
            return func

        return decorator

    def to_group(self):
        def decorator(func):
            self.add_handler(Method.TO_GROUP, func)
            return func

        return decorator

    def ban_get_reason(self):
        def decorator(func):
            self.add_handler(Method.BAN_GET_REASON, func)
            return func

        return decorator

    def bind_chat(self):
        def decorator(func):
            self.add_handler(Method.BIND_CHAT, func)
            return func

        return decorator

    def ignore_messages(self):
        def decorator(func):
            self.add_handler(Method.IGNORE_MESSAGES, func)

        return decorator

    def message_signal(
        self,
        method: Method,
        text: Text,
        lower: bool = False
    ):
        def decorator(func):
            self.add_message_handler(method, func, text, lower)
            return func

        return decorator

    def __repr__(self):
        return (
            f"MESSAGE HANDLERS: {len(self.message_handler)}\n"
            f"EVENT HANDLERS: {len(self.handler)}"
        )

