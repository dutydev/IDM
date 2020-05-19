from aiohttp import web

from dutymanager.db.methods import AsyncDatabase

db = AsyncDatabase().get_current()


async def remove(_db):
    keys = [key for key in _db.keys()]
    for key in keys:
        await _db.remove(key)


async def clean_chats(request: web.Request) -> web.Response:
    data = await request.post()
    await remove(db.chats)

    response = web.json_response({
        'response': 'ok',
        **data
    })
    return response
