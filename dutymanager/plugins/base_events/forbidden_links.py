from module import Blueprint, Method
from module import VKError, types
from dutymanager.units.utils import *
from dutymanager.db.methods import AsyncDatabase

bot = Blueprint()
db = AsyncDatabase.get_current()


@bot.on.event(Method.FORBIDDEN_LINKS)
async def forbidden_links(event: types.ForbiddenLinks):
    """
    TODO: Lil things
    """
    print(event)