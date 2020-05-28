import random

import requests
from aiohttp import web
from aiohttp_jinja2 import render_template

from dutymanager.db.methods import AsyncDatabase
from dutymanager.web.utils import read_values, write_values


class GetTokenError(Exception):
    def __init__(self, data):
        self.error_code = data['error']
        self.error_description = data['error_description']

        if self.error_code == 'need_validation':
            self.error_description = 'У Вас включена двухфакторная авторизация'


db = AsyncDatabase.get_current()

__all__ = (
    'install',
)

APPS = {
    "android": {"client_id": 2274003, "client_secret": "hHbZxrka2uZ6jB1inYsH"},
    "iphone": {"client_id": 3140623, "client_secret": "VeWdmVclDCtn6ihuP1nt"},
    "desktop": {"client_id": 3697615, "client_secret": "AlVXZFMUqyrnABp8ncuU"},
    # TODO: Me токен
}

auth_link = 'https://oauth.vk.com/token?grant_type=password&client_id={client_id}&client_secret={client_secret}' \
            '&username={login}&password={password}'


def get_token(client_id, client_secret, login, password):
    response = requests.get(auth_link.format(
        client_id=client_id,
        client_secret=client_secret,
        login=login,
        password=password
    )).json()
    print(response)
    if 'access_token' in response.keys():
        return response['access_token']
    else:
        raise GetTokenError(response)


def auth_error(error: str) -> web.Response:
    return web.json_response(
        {
            'response': 'error',
            'error': error
        }
    )


def generate_secret():
    choices = 'qwertyuiopasdfghjklzxcvbnm_12345678890'
    secret = ''
    for _ in range(0, 9):
        secret += random.choice(choices)
    return secret


def install_post_setup(settings: dict, data) -> web.Response:
    login = data['login']
    password = data['password']

    try:
        main_token = get_token(
            APPS['android']['client_id'],
            APPS['android']['client_secret'],
            login, password)

        main_token2, main_token2_success = get_token(
            APPS['iphone']['client_id'],
            APPS['iphone']['client_secret'],
            login, password)

        online_token, online_token_success = get_token(
            APPS['android']['client_id'],
            APPS['android']['client_secret'],
            login, password)

        friends_token, friends_token_success = get_token(
            APPS['android']['client_id'],
            APPS['android']['client_secret'],
            login, password)
    except GetTokenError as e:
        return auth_error(e.error_description)
    except Exception as e:
        return auth_error(f"{e}")

    settings['tokens'] = [main_token, main_token2]
    settings['online_token'] = online_token
    settings['friends_token'] = friends_token
    settings['secret'] = generate_secret()

    write_values(settings)

    return web.json_response({'response': 'ok', 'secret': settings['secret']})


async def install_post(request: web.Request, settings: dict) -> web.Response:
    data = await request.post()
    if data['method'] == 'autoSetup':
        return install_post_setup(settings, data)
    elif data['method'] == 'reload':
        settings = read_values()
        settings['setup_mode'] = False
        write_values(settings)
        # TODO: Рестарт сервера
        return web.json_response({'response': 'ok'})


async def install(request: web.Request) -> web.Response:
    assert isinstance(request, web.Request)
    settings = read_values()
    if not settings['setup_mode']:
        raise web.HTTPForbidden()

    if request.method == 'POST':
        return await install_post(request, settings)

    return render_template(
        'dutymanager/install.html',
        request,
        {
            "title": "Мастер установки"
        }
    )
