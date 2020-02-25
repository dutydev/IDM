__version__ = "1.3.2 public" 


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
logger.info(f"Объекты импортированны")

db = objects.DB()
if db.installed:
    logger.info(f"БД настоена Владелец: {db.owner_id} Дежурный: {db.duty_id} Хост: {db.host}")
else:
    logger.info("""БД не настоена""")



from .routes import app
