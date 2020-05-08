from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import get_by_local
from module import Blueprint, Method
from module import types

bot = Blueprint(name="Trusted")
db = AsyncDatabase.get_current()