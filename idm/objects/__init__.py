try:
    from ._version import __version__
except ImportError:
    __version__ = '__blank__'

from .database import DB, DB_general, db_gen

from .events import *

from . import dispatcher as dp
