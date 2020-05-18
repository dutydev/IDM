from aiohttp import web
from aiohttp_jinja2 import render_template


async def handle_5xx(request: web.Request) -> web.Response:
    return render_template(
        'errors/5xx.html',
        request,
        {
            'title': 'Ошибка сервера'
        }
    )
