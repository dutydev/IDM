from aiohttp import web

from dutymanager.web.auth import auth

__all__ = (
    'setup',
)


def create_auth_middleware():
    @web.middleware
    async def error_middleware(request: web.Request, handler):
        await auth.update(request)
        return await handler(request)

    return error_middleware


def setup(app: web.Application):
    app.middlewares.append(create_auth_middleware())
