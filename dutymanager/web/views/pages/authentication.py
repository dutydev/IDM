from aiohttp import web
from aiohttp_jinja2 import render_template

from dutymanager.web.auth import auth
from dutymanager.web.decorators import authenticated_only
from dutymanager.web.forms import LoginForm
from module.utils import logger

__all__ = (
    'login',
    'logout',
)


async def login(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    if request.method == 'POST':
        post_data = await request.post()
        login_form = LoginForm(post_data)
        if await login_form.validate():
            auth.set_user(login_form.user)
            logger.info('Форма валидна')
            response = web.HTTPFound('/')
            response.set_cookie('hash', auth.get_user_hash(auth.get_user()['id'], login_form.data['password']))
            return response

    else:
        login_form = LoginForm()

    return render_template(
        'dutymanager/login.html',
        request,
        {
            'title': "Вход",
            "login_form": login_form
        }
    )


@authenticated_only
async def logout(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    response = web.HTTPFound('/')
    response.del_cookie('hash')
    auth.set_user({})
    return response
