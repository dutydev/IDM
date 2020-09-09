from . import (Event as _Event,
               SignalEvent as _SignalEvent,
               MySignalEvent as _MySignalEvent)
from .handler import handler as _handler

from wtflog import warden as _warden

_logger = _warden.get_boy('Диспетчер callback')


_events = {}
_signal_events = {}
_my_signal_events = {}
_skip_message_receiving = set()


def event_register(method: str):
    def registrator(func):
        _logger.debug(f'Зарегистрирован новый ивент для метода {method}')
        _events.update({method: func})
        return func
    return registrator


def signal_event_register(*commands: tuple):
    def registrator(func):
        _logger.debug(f'Зарегистрирован новый ивент для сигналов к дежурному. Команды {list(commands)}')
        for command in commands:
            _signal_events.update({command: func})
        return func
    return registrator


def my_signal_event_register(*commands: tuple, skip_receiving: bool = False):
    if skip_receiving:  # TODO: перебрать события и добавить этот флаг где возможно
        _skip_message_receiving.add(commands)
    def registrator(func):
        _logger.debug(f'Зарегистрирован новый ивент для сигналов к приемнику. Команды {list(commands)}')
        for command in commands:
            _my_signal_events.update({command: func})
        return func
    return registrator


def event_run(event: _Event):
    if type(event.msg) == int:
        event.set_msg()
    return _handler(event, _events[event.method])


def signal_event_run(event: _SignalEvent):
    event.set_msg()
    _logger.info(f'Обрабатываю ивент {event.method}. Команда: {event.command}')
    if event.command in _signal_events.keys():
        return _handler(event, _signal_events[event.command])
    return {'response': 'error', 'error_code': 2}


def my_signal_event_run(event: _MySignalEvent):
    event.command = event.msg['text'].split(' ')[1]
    if event.command not in _skip_message_receiving:
        event.set_msg()
    _logger.info(f'Обрабатываю ивент {event.method}. Команда: {event.command}')
    if event.command in _my_signal_events.keys():
        return _handler(event, _my_signal_events[event.command])
    return {'response': 'error', 'error_code': 2}


def wrap_handler(wrapper):
    '''Заменяет передаваемый в декорируемую функцию аргумент на результат `wrapper(event)`'''
    def decorate(wrapped):
        def decorator(event: _Event):
            wrap = wrapper(event)
            return wrapped(*wrap if type(wrap) == tuple else wrap)
        return decorator
    return decorate
