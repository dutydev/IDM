from enum import Enum

from aiohttp import web

from dutymanager.web.decorators import authenticated_only

__all__ = (
    'api',
)


class ApiMethod(Enum):
    ADD_TOKEN = 'addToken'
    SET_TOKEN = 'setToken'
    DELETE_TOKEN = 'deleteToken'

    SET_SECRET_CODE = 'setSecretCode'


@authenticated_only
async def api(request: web.Request) -> web.Response:
    post = await request.post()

    method = ApiMethod(post.get('method'))
    return web.json_response({"response": 'ok'})
