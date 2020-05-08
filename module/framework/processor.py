from ..objects.events import Event
from ..utils import logger, sub_string
from .error_handler import ErrorHandler

from vbml import Patcher


class AsyncHandleManager:
    event: Event
    patcher: Patcher
    error_handler: ErrorHandler

    async def _processor(self, event):
        if event["method"] != "ping":
            logger.debug(
                "-> NEW SIGNAL {} FROM CHAT {}",
                event["method"], event["object"]["chat"]
            )

        if event["method"] not in ("sendSignal", "sendMySignal"):
            for handler in self.event.handler:
                if handler.method.value == event["method"]:
                    return await handler(event)

        for handler in self.event.message_handler:
            if handler.method.value == event["method"]:
                for pattern in handler.patterns:
                    text = sub_string(event["message"]["text"])
                    if self.patcher.check(text, pattern) is not None:
                        return await handler(event, **pattern.dict())

    async def error_processor(self, error: Exception, event: dict):
        error_type = error.__class__
        if Exception in self.error_handler.processors:
            return await self.error_handler.notify(error, event)

        if error_type in self.error_handler.processors:
            return await self.error_handler.notify(
                error, event, False
            )

        return False