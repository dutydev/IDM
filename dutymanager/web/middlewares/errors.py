from aiohttp import web

from dutymanager.web.views import errors

__all__ = (
    'setup',
)


def create_error_middleware(overrides: dict):
    @web.middleware
    async def error_middleware(request: web.Request, handler):
        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override:
                return await override(request)
            return response

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)
            raise

    return error_middleware


def setup(app: web.Application):
    middleware = create_error_middleware({
        403: errors.handle_403,
        404: errors.handle_404,
        500: errors.handle_5xx
    })
    app.middlewares.append(middleware)
