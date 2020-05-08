from dutymanager.web.decorators import authenticated_only
from dutymanager.web.objects import WebBlueprint
from dutymanager.web.utils import get_user_hash
from dutymanager.web.forms import LoginForm
from aiohttp_jinja2 import render_template
from module.utils import logger
from aiohttp import web

bot = WebBlueprint()


# TODO: добавить странички 403 404 5xx

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
        login_form = LoginForm(post_data)
        if login_form.validate():
            logger.info('Форма валидна')
            response = web.HTTPFound('/')
            response.set_cookie('hash', get_user_hash(login_form.login, login_form.password))
            return response

    else:
        login_form = LoginForm()

    logger.info(f'{(login_form.errors, login_form.login, login_form.password)}')

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
    return response


@authenticated_only
async def admin(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    web_form = None

    return render_template(
        'dutymanager/admin.html',
        request,
        {
            "form": web_form
        }
    )
