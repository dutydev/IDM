# я тоже ничего разобрать в этой каше не могу, ты не одинок
import re
import time
import json
import traceback
from os import environ
from hashlib import md5
from typing import List, Union

from flask import (Flask, make_response, redirect, render_template,
                   request, send_from_directory, Response)

from idm.utils import gen_secret
from microvk import VkApi, VkApiResponseException
from wtflog import warden

from idm.objects import DB, DB_general, db_gen

if environ.get('FLASK_ENV') == 'development':
    DEBUG = True
else:
    DEBUG = False

app = Flask(__name__)

logger = warden.get_boy(__name__)

auth: str = {
    'token': '',
    'user': 0
    }


class WeHaveAProblem(Exception):
    response: Response

    def __init__(self, response: Response):
        self.response = response


def get_mask(token: str) -> str:
    if len(token) != 85:
        return 'Не установлен'
    return token[:4] + "*" * 77 + token[81:]


def login_check(request) -> None:
    if DEBUG:
        return
    if not db_gen.installed:
        raise WeHaveAProblem(redirect('/install'))
    if request.cookies.get('auth') != auth['token']:
        raise WeHaveAProblem(int_error(
            'Ошибка авторизации, попробуй очистить cookies или перелогиниться'
        ))


def format_tokens(tokens: list) -> List[Union[str, None]]:
    for i in range(len(tokens)):
        token = re.search(r'access_token=[a-z0-9]{85}', tokens[i])
        if token:
            token = token[0][13:]
        elif len(tokens[i]) == 85:
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
            raise WeHaveAProblem(int_error("Неверный токен, попробуй снова"))
    return user_ids


@app.route('/')
def index():
    db = DB_general()
    if db.installed:
        return redirect('/admin')
    return redirect('/install')


@app.route('/auth', methods=["POST"])
def do_auth():
    global auth
    user_id = check_tokens(format_tokens([request.form.get('access_token')]))
    if type(user_id) != list:
        return user_id
    if user_id[0] != db_gen.owner_id:
        return int_error(
            'Вставлен токен от другого аккаунта. Проверь авторизацию ВК'
        )
    response = make_response()
    new_auth = md5(gen_secret().encode()).hexdigest()
    auth['user'] = user_id[0]
    auth['token'] = new_auth
    response.set_cookie("auth", value=new_auth)
    response.headers['location'] = "/"
    return response, 302


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img', 'favicon.png')


@app.route('/install')
def install():
    if db_gen.installed:
        return redirect('/')
    return render_template('pages/install.html')


@app.route('/api/setup_cb', methods=["POST"])
def setup():
    if db_gen.installed:
        return redirect('/')

    tokens = format_tokens([
        request.form.get('access_token')
    ])

    user_id = check_tokens(tokens)[0]
    if type(user_id) != int:
        return user_id

    db_gen.set_user(user_id)
    db = DB()

    db.access_token = tokens[0]

    db.secret = gen_secret()
    db_gen.host = "https://" + request.host
    db_gen.installed = True
    db.trusted_users.append(db.duty_id)
    db.save()
    db_gen.save()
    VkApi(db.access_token).msg_op(
        1, -174105461, f'+api {db.secret} https://{request.host}/callback'
    )
    return redirect('/login')


@app.route('/api/<string:method>', methods=["POST"])
def api(method: str):
    login_check(request)

    db = DB()

    if method == "edit_current_user":
        tokens = format_tokens([
            request.form.get('access_token', ''),
            request.form.get('me_token', '')
        ])
        if tokens[0]:
            db.access_token = tokens[0]
        if tokens[1]:
            db.me_token = tokens[1]
        db.save()

    if method == 'connect_to_iris':
        try:
            VkApi(db.access_token, raise_excepts=True)(
                'messages.send',
                peer_id=-174105461,
                message=f'+api {db.secret} https://{request.host}/callback',
                random_id=0
            )
        except VkApiResponseException as e:
            return int_error(f'Ошибка VK #{e.error_code}: {e.error_msg}')

    if method == "edit_responses":
        for key in db.responses.keys():
            response = request.form.get(key)
            if response:
                db.responses[key] = response
        db.save()
        return redirect('/admin#Responses')

    if method == "edit_dyntemplates":
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
        db.save()
        return redirect('/admin#DynTemplates')

    if method == 'add_dyntemplate':
        db.anims.append({'name': 'анимка',
                         'frames': ['Отсутствует'], 'speed': 1.0})
        db.save()
        return redirect('/admin#DynTemplates')

    if method == 'delete_anim':
        name = request.form['name']
        for i in range(len(db.anims)):
            if db.anims[i]['name'] == name:
                del(db.anims[i])
                db.save()
                return redirect('/admin#DynTemplates')

    if method == 'dc_auth':
        if request.form.get('permit') == 'on':
            db_gen.dc_auth = True
        else:
            db_gen.dc_auth = False
        db_gen.save()

    return redirect('/')


@app.route('/admin')
def admin():
    db_gen = DB_general()

    login_check(request)

    if not db_gen.installed:
        return redirect('/install')

    db = DB()

    warning = None

    users = VkApi(db.access_token)('users.get', user_ids=db.duty_id)
    if type(users) == dict:
        username = 'unknown'
        warning = {'type': 'danger', 'text': 'Ошибка доступа, смени токены'}
    else:
        username = f"{users[0]['first_name']} {users[0]['last_name']}"

    db.access_token = get_mask(db.access_token)
    db.me_token = get_mask(db.me_token)

    return render_template('pages/admin.html', db=db, db_gen=db_gen,
                           users=users, warn=warning, username=username)


@app.route('/login')
def login():
    if not db_gen.installed:
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


@app.errorhandler(WeHaveAProblem)
def oops(e: WeHaveAProblem):
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
