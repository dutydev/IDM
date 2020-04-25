from ..objects.methods import Method
from ..objects.types import BaseObject

from typing import Callable, List, Union
from vbml import Pattern


class Handler:
    def __init__(self, handler: Callable, method: Method):
        self.handler = handler
        self.method = method

    async def __call__(self, event: BaseObject):
        return await self.handler(event)


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
            self.patterns.append(Pattern(x))
        super().__init__(handler, method)

    async def __call__(self, event: BaseObject, **kwargs):
        return await self.handler(event, **kwargs)