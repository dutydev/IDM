from dutymanager.web.utils import is_authenticated
from aiohttp import web

__all__ = (
    'authenticated_only',
)


def authenticated_only(f):
    async def wrapper(request: web.Request, *args, **kwargs) -> web.Response:
        if is_authenticated(request):
            return await f(request, *args, **kwargs)
        else:
            return web.HTTPForbidden()

    return wrapper
