from aiohttp import web
from aiohttp_jinja2 import render_template

from module.utils import logger

__all__ = (
    'help',
)


async def help(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    return render_template(
        'dutymanager/help.html',
        request,
        {
            "title": "Помощь"
        }
    )
