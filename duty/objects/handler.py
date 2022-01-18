from . import Event
from microvk import VkApiResponseException
import traceback

from logger import get_writer
logger = get_writer(__name__)


def handler(event: Event, func):
    logger.info(f"Выполнение команды {event.method}; F:{func.__name__}")
    try:
        return func(event)
    except VkApiResponseException as e:
        data = (f"Ошибка VK\nКод ошибки:{e.error_code}\nСообщение:"
                f"{e.error_msg}\nПараметры:{e.request_params}\n" +
                traceback.format_exc())
        logger.error(data)
        if e.error_code in {5, 6, 14, 924}:
            return {
                "response": "vk_error",
                "error_code": e.error_code,
                "error_message": e.error_msg
            }
        return data
    except Exception:
        data = traceback.format_exc() + '\n\n' + str(event)
        logger.error(data)
        return data
