from module.utils import logger
from typing import Union

Error = Union[Exception, "Any"]


class ErrorHandler:
    def __init__(self):
        self._error_processors = dict()

    def __call__(self, *errors: Error):
        def decorator(func):
            for error in errors:
                self._error_processors[error] = func
            return func

        return decorator

    async def notify(self, error: Exception):
        handler = self.processors[error.__class__]
        logger.debug(
            "{}! Processing it with handler <{}>",
            error.__class__.__name__,
            handler.__name__
        )
        return await handler(error)

    @property
    def processors(self) -> dict:
        return self._error_processors

    def update(self, processors: dict):
        self._error_processors.update(processors)