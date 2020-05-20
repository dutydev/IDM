import os
import sys

from aiohttp import web

from dutymanager.web.utils import write_values
from dutymanager.db.methods import AsyncDatabase

db = AsyncDatabase().get_current()

clean_data = {
    "tokens": None,
    "me_token": None,
    "online_token": None,
    "friends_token": None,
    "secret": None,
    "user_id": None,
    "debug": True,
    "errors_log": True,
    "port": 8080,
    "polling": False
}


async def remove(_db):
    keys = [key for key in _db.keys()]
    for key in keys:
        await _db.remove(key)


async def do_zeroing(request: web.Request) -> web.Response:
    data = await request.post()
    await db.compose()

    await remove(db.chats)
    await remove(db.settings)
    await remove(db.pages)
    await remove(db.templates)
    await remove(db.trusted)
    write_values(clean_data)

    response = web.json_response({
        'response': 'ok',
        **data
    })

    response.cookies.clear()
    return response
