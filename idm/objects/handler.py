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
        data = {
                "тип":"vk_api",
                "код_ошибки":e.error_code,
                "сообщение":e.error_msg,
                "параметры":e.request_params,
                "traceback":traceback.format_exc()
        }
        logger.error(data)
        return data
    except Exception as e:
        data = {
            "тип":e.__class__.__name__,
            "ошибка":f"{e}",
            "traceback":traceback.format_exc()
        }
        logger.error(data)
        return data
    except:
        data = {
            "тип":"неизвестный",
            "traceback":traceback.format_exc()
        }
        logger.error(data)
        return data