import typing
from . import Methods, Event, SignalEvent, MySignalEvent
import logging

logger = logging.getLogger(__name__)


class Handler:
    method: Methods
    f: typing.Callable
    
    def __init__(self, method: typing.Union[Methods, str], f: typing.Callable):
        self.method = Methods(method)
        self.f = f

    def __call__(self, event: Event) -> typing.Union[str, dict]:
        logger.info(f"Выполнение команды {self.method.value}; F:{self.f.__name__}")
        try:
            return self.f(event)
        except Exception as e:
            return {"error": str(e)}


class SignalHandler:
    commands: typing.List[str]
    f: typing.Callable

    def __init__(self, commands: typing.List[str], f: typing.Callable):
        self.commands = commands
        self.f = f

    def __call__(self, event: SignalEvent):
        try:
            logger.info(f"Выполнение команды {event.command}; F:{self.f.__name__}")
            return self.f(event)
        except Exception as e:
            return {"error": str(e)}
    

class MySignalHandler:
    commands: typing.List[str]
    f: typing.Callable

    def __init__(self, commands: typing.List[str], f: typing.Callable):
        self.commands = commands
        self.f = f

    def __call__(self, event: MySignalEvent):
        try:
            logger.info(f"Выполнение команды {event.command}; F:{self.f.__name__}")
            return self.f(event)
        except Exception as e:
            return {"error": str(e)}