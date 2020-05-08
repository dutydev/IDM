from typing import Dict, Callable
from module.utils import logger


class ErrorHandler:
    def __init__(self):
        self._error_processors: Dict[Exception, Callable] = dict()

    def __call__(self, *errors: Exception):
        def decorator(func):
            for error in errors:
                self._error_processors[error] = func
            return func

        return decorator

    async def notify(
        self,
        error: Exception,
        event: dict,
        ignore: bool = True
    ):
        name = Exception if ignore else error.__class__
        handler = self.processors[name]
        logger.debug(
            "{}! Processing it with handler <{}>",
            error.__class__.__name__,
            handler.__name__
        )
        return await handler(error, event)

    @property
    def processors(self) -> dict:
        return self._error_processors

    def update(self, processors: dict):
        self._error_processors.update(processors)