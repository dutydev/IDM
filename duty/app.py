import re
import time
import json
import traceback

from os import environ
from hashlib import md5
from typing import List, Union

from flask import (Flask, make_response, redirect, render_template,
                   request, send_from_directory, Response)

from duty.utils import gen_secret
from microvk import VkApi, VkApiResponseException
from logger import get_writer

from duty.objects import db


DEBUG = (environ.get('FLASK_ENV') == 'development')

app = Flask(__name__)

logger = get_writer('Веб-приложение')



class ReturnResponse(Exception):
    response: Response

    def __init__(self, response: Response):
        self.response = response


def get_mask(token: str) -> str:
    if len(token) == 0:
        return 'Не установлен'
    return token[:4] + "*" * 77 + token[81:]


def login_check(request) -> None:
    if DEBUG:
        return
    if not db.installed:
        raise ReturnResponse(redirect('/install'))
    if request.cookies.get('auth') == db.auth_token:
        if time.time() - db.auth_token_date < 86400:
            return
    raise ReturnResponse(int_error(
        'Ошибка авторизации, попробуй очистить cookies или перелогиниться'
    ))


def format_tokens(tokens: list) -> List[Union[str, None]]:
    for i in range(len(tokens)):
        token = re.search(r'access_token=vk1.a.[^.]{192}&', tokens[i])
        if token:
            token = token[0][13:192]
        elif len(tokens[i]) > 0:
            token = tokens[i]
        else:
            token = None
        tokens[i] = token
    return tokens


def check_tokens(tokens: list):
    user_ids = []
    for i in range(len(tokens)):
        try:
            user_ids.append(
                VkApi(tokens[i], raise_excepts=True)('users.get')[0]['id']
            )
            time.sleep(0.4)
        except VkApiResponseException:
            raise ReturnResponse(int_error("Неверный токен, попробуй снова"))
    return user_ids


@app.route('/')
def index():
    if db.installed:
        return redirect('/admin')
    return redirect('/install')


@app.route('/auth', methods=["POST"])
def do_auth():
    user_id = check_tokens(format_tokens([request.form.get('access_token')]))
    if type(user_id) != list:
        return user_id
    if user_id[0] != db.owner_id:
        return int_error(
            'Вставлен токен от другого аккаунта. Проверь авторизацию ВК'
        )
    response = make_response()
    db.auth_token = md5(gen_secret().encode()).hexdigest()
    db.auth_token_date = int(time.time())
    response.set_cookie("auth", value=db.auth_token)
    response.headers['location'] = "/"
    db.sync()
    return response, 302


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img', 'favicon.png')


@app.route('/install')
def install():
    if db.installed:
        return redirect('/')
    return render_template('pages/install.html')


@app.route('/api/setup_cb', methods=["POST"])
def setup():
    if db.installed:
        return redirect('/')

    tokens = format_tokens([
        request.form.get('access_token')
    ])

    user_id = check_tokens(tokens)[0]
    if type(user_id) != int:
        return user_id

    db.owner_id = user_id

    db.access_token = tokens[0]

    db.secret = gen_secret()
    db.host = "https://" + request.host
    db.installed = True
    db.trusted_users.append(db.owner_id)
    protocol = 'https' if 'pythonanywhere' in request.host else 'http'
    VkApi(db.access_token).msg_op(
        1, -174105461, f'+api {db.secret} {protocol}://{request.host}/callback'
    )
    return do_auth()


@app.route('/api/<string:method>', methods=["POST"])
def api(method: str):
    login_check(request)
    handler = globals().get(f'app_method_{method}', lambda: None)
    result = handler()
    db.sync()
    return result or redirect('/')


def app_method_edit_current_user():
    tokens = format_tokens([
        request.form.get('access_token', ''),
        request.form.get('me_token', '')
    ])
    if tokens[0]:
        db.access_token = tokens[0]
    if tokens[1]:
        db.me_token = tokens[1]


def app_method_connect_to_iris():
    try:
        protocol = 'https' if 'pythonanywhere' in request.host else 'http'
        VkApi(db.access_token, raise_excepts=True)(
            'messages.send',
            peer_id=-174105461,
            message=f'+api {db.secret} {protocol}://{request.host}/callback',
            random_id=0
        )
    except VkApiResponseException as e:
        return int_error(f'Ошибка VK #{e.error_code}: {e.error_msg}')


def app_method_edit_responses():
    for key, response in request.form.items():
        if response:
            db.responses[key] = response
    return redirect('/admin#Responses')


def app_method_edit_dyntemplates():
    name = request.form['temp_name']
    length = int(request.form['length'])
    i = 0
    frames = []
    while True:
        if i >= length:
            break
        frame = request.form.get(f'frame{i}')
        if frame:
            frames.append(frame)
        elif i < length:
            frames.append('Пустой кадр')
        else:
            break
        i += 1
    temp = {'name': request.form['new_name'].lower(),
            'frames': frames, 'speed': float(request.form['speed'])}
    for i in range(len(db.anims)):
        if db.anims[i]['name'] == name:
            db.anims[i].update(temp)
            break
    return redirect('/admin#DynTemplates')


def app_method_add_dyntemplate():
    db.anims.append({'name': 'анимка',
                        'frames': ['Отсутствует'], 'speed': 1.0})
    return redirect('/admin#DynTemplates')


def app_method_delete_anim():
    name = request.form['name']
    for i in range(len(db.anims)):
        if db.anims[i]['name'] == name:
            del(db.anims[i])
            return redirect('/admin#DynTemplates')


@app.route('/admin')
def admin():
    login_check(request)

    if not db.installed:
        return redirect('/install')

    warning = None

    users = VkApi(db.access_token)('users.get', user_ids=db.owner_id)
    if type(users) == dict:
        username = 'НЕИЗВЕСТНЫЙ ПОЛЬЗОВАТЕЛЬ'
        warning = {'type': 'danger', 'text': 'Ошибка доступа, смени токены'}
    else:
        username = f"{users[0]['first_name']} {users[0]['last_name']}"

    access_token = get_mask(db.access_token)
    me_token = get_mask(db.me_token)

    return render_template('pages/admin.html', db=db, access_token=access_token,
                           users=users, warn=warning, username=username,
                           me_token=me_token)


@app.route('/login')
def login():
    if not db.installed:
        return redirect('/')
    return render_template('pages/login.html')


@app.errorhandler(404)
def page_not_found(_):
    return render_template('errors/404.html'), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return render_template('errors/404.html'), 405


@app.errorhandler(500)
def int_error(e):
    return render_template('errors/500.html', error=e), 500


@app.errorhandler(ReturnResponse)
def oops(e: ReturnResponse):
    return e.response


@app.errorhandler(Exception)
def on_error(e: Exception):
    logger.error(f'Ошибка при обработке запроса:\n' +
                 traceback.format_exc())
    return f'Неизвестная ошибка:\n{e.__class__.__name__}: {e}'


@app.errorhandler(json.decoder.JSONDecodeError)
def decode_error(e):
    logger.error(f'Ошибка при декодировании данных:\n{e}\n{traceback.format_exc()}')  # noqa
    return ('Произошла ошибка при декодировании JSON (скорее всего в файлах '
            ' БД), проверь файлы в ICAD/database<br>Место, где споткнулся '
            f'декодер: {e}')
