from . import Event, SignalEvent, MySignalEvent

from .handler import handler

from wtflog import warden

logger = warden.get_boy(__name__)


class Dispatcher:

    events = {}
    signal_events = {}
    my_signal_events = {}

    def event_register(self, method: str, func):
        logger.debug(f'Зарегистрирован новый ивент для метода {method}')
        self.events.update({method: func})

    def event_handle(self, method: str):
        def decorator(func):
            self.event_register(method, func)
        return decorator

    def event_run(self, event: Event):
        return handler(event, self.events[event.method])


    def signal_event_register(self, *args: tuple):
        def decorator(func):
            logger.debug(f'Зарегистрирован новый ивент для сигналов к дежурному. Команды {list(args)}')
            for command in args:
                self.signal_events.update({command: func})
        return decorator

    def signal_event_run(self, event: SignalEvent):
        logger.info(f'Обрабатываю ивент {event.method}. Команда: {event.command}')
        if event.command in self.signal_events.keys():
            return handler(event, self.signal_events[event.command])
        return {'response': 'error', 'error_code': 2}


    def my_signal_event_register(self, *args: tuple):
        def decorator(func):
            logger.debug(f'Зарегистрирован новый ивент для сигналов к приемнику. Команды {list(args)}')
            for command in args:
                self.my_signal_events.update({command: func})
        return decorator

    def my_signal_event_run(self, event: MySignalEvent):
        logger.info(f'Обрабатываю ивент {event.method}. Команда: {event.command}')
        if event.command in self.my_signal_events.keys():
            return handler(event, self.my_signal_events[event.command])
        return {'response': 'error', 'error_code': 2}


dp = Dispatcher()
    