from aiohttp import web
from aiohttp_jinja2 import render_template


async def handle_404(request: web.Request) -> web.Response:
    return render_template(
        'errors/404.html',
        request,
        {
            'title': 'Страница не найдена'
        }
    )
