from dutymanager.db.methods import AsyncDatabase
from module import Blueprint, Method
from dutymanager.units.utils import *
from module import VKError, types

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.event.forbidden_links()
async def forbidden_links(event: types.ForbiddenLinks):
    """
    TODO: Lil things
    """
    print(event)