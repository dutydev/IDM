from aiohttp import web
from aiohttp_jinja2 import render_template

from dutymanager.web.decorators import authenticated_only
from dutymanager.web.utils import read_values

__all__ = (
    'admin',
)


@authenticated_only
async def admin(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    web_form = None

    settings = read_values()
    settings['tokens'] = settings['tokens'] if isinstance(settings['tokens'], list) else [settings['tokens']]

    return render_template(
        'dutymanager/admin.html',
        request,
        {
            'title': 'Панель управления',
            "form": web_form
        }
    )
