from aiohttp import web
from aiohttp_jinja2 import render_template
from dutymanager.web import forms
from module.utils import logger


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


async def login(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    logger.info(f'{request.method} -> {request.path}')
    if request.method == 'POST':
        post_data = await request.post()
        login_form = forms.LoginForm(post_data)
        if login_form.validate():
            logger.info('Форма валидна')
            raise web.HTTPFound('/')
    else:
        login_form = forms.LoginForm()

    logger.info(f'{(login_form.errors, login_form.login, login_form.password)}')

    return render_template(
        'dutymanager/login.html',
        request,
        {
            'title': "Вход",
            "login_form": login_form
        }
    )
