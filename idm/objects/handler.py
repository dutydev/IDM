import typing
from . import Event, SignalEvent, MySignalEvent
from microvk import VkApiResponseException
import traceback

from wtflog import warden
logger = warden.get_boy(__name__)


def handler(event: Event, func):
    logger.info(f"Выполнение команды {event.method}; F:{func.__name__}")
    try:
        return func(event)
    except VkApiResponseException as e:
        data = f"Ошибка VK\nКод ошибки:{e.error_code}\nСообщение:{e.error_msg}\nПараметры:{e.request_params}\n{traceback.format_exc()}"
        logger.error(data)
        return data
    except Exception as e:
        data = traceback.format_exc()
        logger.error(data)
        return data
    except:
        data = traceback.format_exc()
        logger.error(data)
        return data