import os
from wtflog import warden

logger = warden.setup(os.path.join(os.path.dirname(os.path.dirname(__file__)), f"duty.log"),
        level = warden.INFO, clear_on_start = 'backup')
logger.info('Запуск IDM...')
from . import objects, api_utils, utils, commands
from .routes import app
from .objects import db_gen as db, __version__

from .remote_control import __name__
