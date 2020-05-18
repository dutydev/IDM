from aiohttp import web
from aiohttp_jinja2 import render_template

from module.utils import logger

__all__ = (
    'index',
)


async def index(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    logger.info(f'{request.method} -> {request.path}')
    return render_template(
        'dutymanager/index.html',
        request,
        {
            "title": "Главная"
        }
    )
