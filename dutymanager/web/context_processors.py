from dutymanager.web.utils import is_authenticated as is_auth
from dutymanager.web.objects import WebBlueprint
from aiohttp import web

bot = WebBlueprint()


async def auth_user_ctx_processor(request: web.Request) -> dict:
    is_authenticated = is_auth(request)
    current_user = {}
    if is_authenticated:
        current_user = {
            "id": bot.user_id
            # TODO: Добавить инфу о юзвере
        }
    return {
        'user': {
            'is_anonymous': not is_authenticated,
            'is_authenticated': is_authenticated,
            'info': current_user
        }
    }
