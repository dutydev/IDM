from ..objects.events import Event
from ..utils import logger, sub_string
from .error_handler import ErrorHandler

from vbml import Patcher


class AsyncHandleManager:
    event: Event
    error_handler: ErrorHandler
    _patcher: Patcher

    async def _processor(self, event: dict):
        method = event["method"]
        if method != "ping":
            logger.debug(
                "-> NEW SIGNAL {} FROM CHAT {}",
                method, event["object"]["chat"]
            )

        if method in ("sendSignal", "sendMySignal"):
            return await self.message_processor(event)

        if method in self.event.routes:
            return await self.event.routes[method](event)

    async def message_processor(self, event: dict):
        """
        TODO: Adding Routing to Increase Performance
        """
        for handler in self.event.message_handler:
            if handler.method.value == event["method"]:
                for pattern in handler.patterns:
                    text = sub_string(event["message"]["text"])
                    if self._patcher.check(text, pattern) is not None:
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