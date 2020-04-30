from ..objects.methods import Method
from ..objects.types import BaseObject

from typing import Callable, List, Union
from inspect import getfullargspec
from vbml import Pattern
from re import IGNORECASE


class Handler:
    def __init__(self, handler: Callable, method: Method):
        self.handler = handler
        self.method = method
        self.args = getfullargspec(handler).annotations
        if not issubclass(self.args["event"], BaseObject):
            raise AttributeError(
                f'Value should be instance of BaseObject not {self.args["event"].__name__!r}'
            )

    async def __call__(self, event: dict):
        dataclass = self.args["event"](**event)
        return await self.handler(dataclass)


class MessageHandler(Handler):
    def __init__(
        self,
        handler: Callable,
        method: Method,
        text: Union[str, List[str]],
        lower: bool
    ):
        self.patterns: List[Pattern] = list()
        self.lower = lower
        text = text if isinstance(text, list) else [text]
        for x in text:
            self.patterns.append(
                Pattern(x, flags=IGNORECASE if lower else None)
            )
        super().__init__(handler, method)

    async def __call__(self, event: dict, **kwargs):
        dataclass = self.args["event"](**event)
        return await self.handler(dataclass, **kwargs)
