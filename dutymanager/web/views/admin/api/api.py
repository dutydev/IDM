from enum import Enum

from aiohttp import web

from dutymanager.web.decorators import authenticated_only

from dutymanager.web.views.admin.api import methods

__all__ = (
    'api',
)


class ApiMethod(Enum):
    ADD_TOKEN = 'addToken'
    SET_TOKEN = 'setToken'
    DELETE_TOKEN = 'deleteToken'
    SET_SECRET_CODE = 'setSecretCode'

    DO_ZEROING = 'doZeroing'
    DO_ZEROING_CHATS = 'doZeroingChats'


@authenticated_only
async def api(request: web.Request) -> web.Response:
    post = await request.post()

    method = ApiMethod(post.get('method'))

    if method == ApiMethod.DO_ZEROING:
        return await methods.do_zeroing(request)
    elif method == ApiMethod.DO_ZEROING_CHATS:
        return await methods.clean_chats(request)

    return web.json_response(
        {
            "response": 'ok'
        }
    )
