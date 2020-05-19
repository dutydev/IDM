from aiohttp import web
from module.utils import logger

from dutymanager.web.auth import auth

__all__ = (
    'setup',
)


def create_logging_middleware():
    @web.middleware
    async def logging_middleware(request: web.Request, handler):

        logger.info(
            f"{request.remote} | {request.method} -> {request.path_qs}"
        )

        return await handler(request)
    return logging_middleware


def setup(app: web.Application):
    app.middlewares.append(create_logging_middleware())
