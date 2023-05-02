from . import (Event as _Event,
               SignalEvent as _SignalEvent,
               MySignalEvent as _MySignalEvent,
               LongpollEvent as _LongpollEvent)
from .handler import handler as _handler

from logger import get_writer as _get_writer

_logger = _get_writer('Диспетчер callback')


_events = {}
_signal_events = {}
_my_signal_events = {}
_skip_message_receiving = set()
_longpoll_events = {}


def event_register(method: str):
    def registrator(func):
        _logger.debug(f'Зарегистрирован обработчик для метода {method}')
        _events.update({method: func})
        return func
    return registrator


def signal_event_register(*commands: str):
    def registrator(func):
        _logger.debug(f'Зарегистрирована новая команда для сигналов к ' +
                      f'дежурному. Команды {list(commands)}')
        for command in commands:
            _signal_events.update({command: func})
        return func
    return registrator


def my_signal_event_register(*commands: str, skip_receiving: bool = False):
    def registrator(func):
        _logger.debug(f'Зарегистрирована новая команда для сигналов к ' +
                      f'приемнику. Команды {list(commands)}')
        for command in commands:
            _my_signal_events.update({command: func})
        return func
    if skip_receiving:
        _skip_message_receiving.add(commands)
    return registrator


def longpoll_event_register(*commands: str):
    def registrator(func):
        _logger.debug(f'Зарегистрирована новая команда для сигналов к ' +
                      f'LP приемнику. Команды {list(commands)}')
        for command in commands:
            _longpoll_events.update({command: func})
        return func
    return registrator


def event_run(event: _Event):
    if type(event.msg) == int:
        event.set_msg()
    return _handler(event, _events[event.method])


def signal_event_run(event: _SignalEvent):
    event.set_msg()
    _logger.info(f'Обрабатываю событие {event.method}')
    if event.command in _signal_events.keys():
        return _handler(event, _signal_events[event.command])
    return {'response': 'error', 'error_code': 2}


def my_signal_event_run(event: _MySignalEvent):
    event.command = event.msg['text'].split(' ')[1]
    if event.command not in _skip_message_receiving:
        event.set_msg()
    _logger.info(f'Обрабатываю событие {event.method}.' +
                 f'Команда: {event.command}')
    if event.command in _my_signal_events.keys():
        return _handler(event, _my_signal_events[event.command])
    return {'response': 'error', 'error_code': 2}


def longpoll_event_run(event: _LongpollEvent):
    _logger.info(f'Обрабатываю событие {event.method}.' +
                 f'Команда: {event.command}')
    if event.command in _longpoll_events.keys():
        return _handler(event, _longpoll_events[event.command])


def wrap_handler(wrapper):
    '''Заменяет передаваемый в декорируемую функцию аргумент на результат
    `wrapper(event)`'''
    def decorate(wrapped):
        def decorator(event: _Event):
            wrap = wrapper(event)
            return wrapped(*wrap if type(wrap) == tuple else wrap)
        return decorator
    return decorate
