import os
from wtflog import warden

logger = warden.setup(os.path.join(os.path.dirname(os.path.dirname(__file__)), f"idm.log"),
        level = warden.INFO, clear_on_start = 'backup')
logger.info('Запуск IDM...')
from . import objects, utils, commands, sync
from .routes import app
from .objects import db_gen as db, __version__
from .lpcommands.utils import send_info


if db.installed:
    if db.v_last != __version__:
        send_info(f'Я обновил твоего дежурного, новая версия: {__version__}')
        db.v_last = __version__
        db.save()