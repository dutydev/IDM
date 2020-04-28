from aiohttp import web
from aiohttp_jinja2 import render_template
from dutymanager.web import forms


async def index(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    return render_template(
        'dutymanager/index.html',
        request,
        {
            "title": "Главная"
        }
    )


async def login(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    if request.method == 'POST':
        post_data = await request.post()
        login_form = forms.LoginForm(post_data)
    else:
        login_form = forms.LoginForm()

    return render_template(
        'dutymanager/login.html',
        request,
        {
            'title': "Вход",
            "login_form": login_form
        }
    )
