from aiohttp import web
from aiohttp_jinja2 import render_template

from dutymanager.db.methods import AsyncDatabase
from dutymanager.web.decorators import authenticated_only
from dutymanager.web.utils import read_values

__all__ = (
    'admin',
)

db = AsyncDatabase().get_current()


@authenticated_only
async def admin(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)

    settings = read_values()
    settings['tokens'] = settings['tokens'] if isinstance(settings['tokens'], list) else [settings['tokens']]

    return render_template(
        'dutymanager/admin.html',
        request,
        {
            'title': 'Панель управления',
            'settings': settings,
            'db': db
        }
    )
