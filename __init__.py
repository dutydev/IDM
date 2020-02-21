__version__ = "1.3 0001"


import logging
import os

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"idm.log")
logging.basicConfig(handlers=[logging.FileHandler(path, 'a', 'utf-8')], level=logging.WARNING,
    format="%(asctime)s:%(levelname)s:[%(module)s]:[th:%(threadName)s|fn:%(funcName)s]:%(message)s")


from . import objects, utils, commands

from .routes import app
