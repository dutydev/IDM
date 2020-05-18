from aiohttp import web

from dutymanager.web.auth import auth

__all__ = (
    'authenticated_only',
)


def authenticated_only(f):
    async def wrapper(request: web.Request, *args, **kwargs) -> web.Response:
        if auth.is_authenticated(request):
            return await f(request, *args, **kwargs)
        else:
            return web.HTTPForbidden()

    return wrapper
