from aiohttp import web
from aiohttp_jinja2 import render_template


async def handle_403(request: web.Request) -> web.Response:
    return render_template(
        'errors/403.html',
        request,
        {
            'title': 'Нет доступа'
        }
    )
