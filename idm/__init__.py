from os.path import join, dirname
from wtflog import warden

logger = warden.setup(join(dirname(dirname(__file__)), f"duty.log"),
                      level=warden.INFO, clear_on_start='backup')

from .app import app
from idm.objects import db_gen as db, __version__

from .iris_listener import __name__
from .icad_listener import __name__
from .longpoll_listener import __name__

from .my_signals import __name__
from .callback_signals import __name__
from .longpoll_signals import __name__
