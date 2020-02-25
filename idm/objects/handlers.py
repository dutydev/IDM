import typing
from . import Methods, Event, SignalEvent, MySignalEvent
import logging
from vkapi import VkApiResponseException
import traceback

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
        except VkApiResponseException as e:
            data = {
                    "тип":"vk_api",
                    "код_ошибки":e.error_code,
                    "сообщение":e.error_msg,
                    "параметры":e.request_params,
                    "traceback":traceback.format_exc()
            }
            logger.exception(data)
            return data
        except Exception as e:            
            data = {
                "тип":e.__class__.__name__,
                "ошибка":f"{e}",
                "traceback":traceback.format_exc()
            }
            logger.exception(data)
            return data
        except:                       
            data = {
                "тип":"неизвесный",
                "traceback":traceback.format_exc()
            }
            logger.exception(data) 
            return data

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
        except VkApiResponseException as e:
            data = {
                    "тип":"vk_api",
                    "код_ошибки":e.error_code,
                    "сообщение":e.error_msg,
                    "параметры":e.request_params,
                    "traceback":traceback.format_exc()
            }
            logger.exception(data)
            return data
        except Exception as e:            
            data = {
                "тип":e.__class__.__name__,
                "ошибка":f"{e}",
                "traceback":traceback.format_exc()
            }
            logger.exception(data)
            return data
        except:                       
            data = {
                "тип":"неизвесный",
                "traceback":traceback.format_exc()
            }
            logger.exception(data) 
            return data
    

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
        except VkApiResponseException as e:
            data = {
                    "тип":"vk_api",
                    "код_ошибки":e.error_code,
                    "сообщение":e.error_msg,
                    "параметры":e.request_params,
                    "traceback":traceback.format_exc()
            }
            logger.exception(data)
            return data
        except Exception as e:            
            data = {
                "тип":e.__class__.__name__,
                "ошибка":f"{e}",
                "traceback":traceback.format_exc()
            }
            logger.exception(data)
            return data
        except:                       
            data = {
                "тип":"неизвесный",
                "traceback":traceback.format_exc()
            }
            logger.exception(data) 
            return data