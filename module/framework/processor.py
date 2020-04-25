from ..objects.events import Event
from ..utils import logger, sub_string

from vbml import Patcher, Pattern


class AsyncHandleManager:
    on: Event

    async def _processor(self, event, patcher: Patcher):
        if event.method != "ping":
            logger.debug(
                "-> NEW SIGNAL {} FROM CHAT {}",
                event.method, event.object.chat
            )

        if event.method not in ("sendSignal", "sendMySignal"):
            for handler in self.on.handler:
                if handler.method.value == event.method:
                    return await handler(event)

        for handler in self.on.message_handler:
            if handler.method.value == event.method:
                for pattern in handler.patterns:
                    text = sub_string(
                        event.message.text if not handler.lower
                        else event.message.text.lower()
                    )
                    if patcher.check(text, pattern) is not None:
                        return await handler(event, **pattern.dict())

