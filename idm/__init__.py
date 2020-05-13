__version__ = "1.0.4 (1.3.2 public)"

import logging
import os

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"idm.log")
logging.basicConfig(handlers=[
    logging.FileHandler(path, 'a', 'utf-8'),
    logging.StreamHandler()
    ], level=logging.ERROR,
    format="%(asctime)s:%(levelname)s:[%(module)s]:[th:%(threadName)s|fn:%(funcName)s]:%(message)s")




logger = logging.getLogger("IDMStart")

logger.info(f"Запускаю IDM v{__version__}")

from . import objects, utils, commands
logger.info(f"Объекты импортированы")

db = objects.DB()
if db.installed:
    logger.info(f"БД настроена Владелец: {db.owner_id} Дежурный: {db.duty_id} Хост: {db.host}")
else:
    logger.info("""БД не настроена""")



from .routes import app

from .objects import DB
from .lp import IIS
db = DB()
if db.installed:
    if db.v_last != __version__:
        IIS(f'Я обновил твоего дежурного, новая версия: {__version__}')
        db.v_last = __version__
        db.save()