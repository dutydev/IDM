from ...utils import new_msg
from ..objects import Event
#event.api("messages.send", random_id=0, chat_id='39ceec24')
new_msg('<vkapi.api.VkApi object at 0x7fb324856550>', '2000000143', message='ПРОВЕРКА ЕЖЕДНЕВНЫХ ЗАДАЧ ПИТОНАНИВЕРЕ\nЕБИТЬ ЕГО В СРАКУ')
import logging
logger = logging.getLogger(__name__)
logger.info("Задача отработала")
#return "ok"