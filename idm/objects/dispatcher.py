import typing
from . import Methods, Handler, SignalHandler, MySignalHandler, \
                Event, SignalEvent, MySignalEvent

import logging

logger = logging.getLogger(__name__)



class Dispatcher:
    Methods: Methods

    event_handlers: typing.List[Handler]
    signal_event_handlers: typing.List[SignalHandler]
    my_signal_event_handlers: typing.List[MySignalHandler]

    def __init__(self):
        self.Methods = Methods

        self.event_handlers = []
        self.signal_event_handlers = []
        self.my_signal_event_handlers = []

    def event_register(self, method: typing.Union[Methods, str], f: typing.Callable):
        logger.debug(f'Зарегистрирован новый ивент для метода {method.value}')
        self.event_handlers.append(Handler(method, f))        

    def event_handle(self, method: typing.Union[Methods, str]) -> typing.WrapperDescriptorType:
        def decorator(f: typing.Callable):
            self.event_register(method, f)
        return decorator

    def event_run(self, event: Event) -> typing.Iterable[typing.Union[str, dict]]:
        for handler in self.event_handlers:
            if handler.method == event.method:
                yield handler(event)


    def signal_event_register(self, commands: typing.List[str], f: typing.Callable):
        logger.debug(f'Зарегистрирован новый ивент для сигналов к дежурному. Команды {commands}')
        self.signal_event_handlers.append(SignalHandler(commands, f))

    def signal_event_handle(self, *args: typing.Tuple[str]) -> typing.WrapperDescriptorType:
        def decorator(f: typing.Callable):
            self.signal_event_register(list(args), f)
        return decorator

    def signal_event_run(self, event: SignalEvent) -> typing.Iterable[typing.Union[str, dict]]:
        logger.info(f'Обрабатываю ивент {event.method.value}. Команда: {event.command}')
        for handler in self.signal_event_handlers:
            if event.command.lower() in handler.commands:
                yield handler(event)


    def my_signal_event_register(self, commands: typing.List[str], f: typing.Callable):
        logger.debug(f'Зарегистрирован новый ивент для сигналов к приемнику. Команды {commands}')
        self.my_signal_event_handlers.append(MySignalHandler(commands, f))

    def my_signal_event_handle(self, *args: typing.Tuple[str]) -> typing.WrapperDescriptorType:
        def decorator(f: typing.Callable):
            self.my_signal_event_register(list(args), f)
        return decorator

    def my_signal_event_run(self, event: MySignalEvent) -> typing.Iterable[typing.Union[str, dict]]:
        logger.info(f'Обрабатываю ивент {event.method.value}. Команда: {event.command}')
        for handler in self.my_signal_event_handlers:
            if event.command.lower() in handler.commands:
                yield handler(event)


dp = Dispatcher()
    