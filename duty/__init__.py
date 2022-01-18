from os.path import join, dirname

from .app import app
from duty.objects import __version__

from .iris_listener import __name__
from .icad_listener import __name__
from .longpoll_listener import __name__

from .my_signals import __name__
from .callback_signals import __name__
from .longpoll_signals import __name__
