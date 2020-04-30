from module import Blueprint, Method
from module import types
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import get_by_local

bot = Blueprint(name="Trusted")
db = AsyncDatabase.get_current()





