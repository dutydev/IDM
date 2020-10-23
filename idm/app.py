# я тоже ничего разобрать в этой каше не могу, ты не одинок
import re
import time
import json
import traceback
from os import environ
from hashlib import md5
from typing import List, Union

from flask import (Flask, make_response, redirect, render_template, request,
                   send_from_directory, Request)

from idm.utils import gen_secret
from microvk import VkApi, VkApiResponseException
from wtflog import warden

from idm.objects import DB, DB_general, ExcDB, db_gen

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


def get_mask(token: str) -> str:
    if len(token) != 85:
        return 'Не установлен'
    return token[:4] + "*" * 77 + token[81:]


def login_check(request, db: DB, db_gen: DB_general) -> Union[Request, None]:
    if DEBUG:
        return
    # uid = db.duty_id TODO: убрать авторизацию вк, не буду возвращать уже
    # token = request.cookies.get('token')
    if not db_gen.installed:
        return redirect('/install')
    # if md5(f"{db_gen.vk_app_id}{uid}{db_gen.vk_app_secret}".encode()).hexdigest() != token:
    if request.cookies.get('auth') != auth['token']:
        return int_error('Ошибка авторизации, попробуй очистить cookies или перелогиниться')


def format_tokens(tokens: list) -> List[Union[str, None]]:
    for i in range(len(tokens)):
        token = re.search(r'access_token=[a-z0-9]{85}', tokens[i])
        if token: token = token[0][13:]
        elif len(tokens[i]) == 85: token = tokens[i]
        else: token = None
        tokens[i] = token
    return tokens


def check_tokens(tokens: list):
    user_ids = []
    for i in range(len(tokens)):
        try:
            user_ids.append(VkApi(tokens[i], raise_excepts=True)('users.get')[0]['id'])
            time.sleep(0.4)
        except VkApiResponseException:
            return int_error("Неверный токен, попробуйте снова")
    return user_ids


@app.route('/')
def index():
    db = DB_general()
    if db.installed: return redirect('/admin')
    return redirect('/install')


@app.route('/auth', methods=["POST"])
def do_auth():
    global auth
    user_id = check_tokens(format_tokens([request.form.get('access_token')]))
    if type(user_id) != list: return user_id
    auth['user'] = user_id[0]
    DB(user_id[0])  # ловим исключение, если юзер не в БД
    response = make_response()
    new_auth = md5(gen_secret().encode()).hexdigest()
    auth['token'] = new_auth
    response.set_cookie("auth", value=new_auth)
    response.headers['location'] = "/"
    return response, 302


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img', 'favicon.png')


@app.route('/install')
def install():
    db = DB_general()
    if db.installed: return redirect('/')
    return render_template('pages/install.html')


@app.route('/api/<string:method>', methods=["POST"])
def api(method: str):
    if method == "setup_cb":#--------------------------------------------------------------
        if db_gen.installed: return redirect('/')
        
        tokens = format_tokens([request.form.get('access_token'), request.form.get('me_token')])
        
        user_id = check_tokens(tokens)[0]
        if type(user_id) != int: return user_id

        db_gen.set_user(user_id)
        db = DB(user_id)


        db.access_token = tokens[0]
        db.me_token = tokens[1]
        
        db.secret = gen_secret()
        # db_gen.vk_app_id = int(request.form.get('vk_app_id'))
        # db_gen.vk_app_secret = request.form.get('vk_app_secret')
        db_gen.host = "http://" + request.host
        db_gen.installed = True
        db.trusted_users.append(db.duty_id)
        db.save()
        db_gen.save()
        return redirect('/login?next=/admin')


    db = DB(auth['user'])

    login = login_check(request, db, db_gen)
    if login: return login


    if method == "edit_current_user":#--------------------------------------------------------------
        tokens = format_tokens([
            request.form.get('access_token', ''),
            request.form.get('me_token', '')
        ])
        if tokens[0]: db.access_token = tokens[0]
        if tokens[1]: db.me_token = tokens[1]
        db.save()
        return redirect('/admin')


    if method == 'connect_to_iris':
        try:
            VkApi(db.access_token, raise_excepts=True)('messages.send', random_id = 0,
                message = f'+api {db.secret} {db.gen.host}/callback', peer_id = -174105461)
        except VkApiResponseException as e:
            return int_error(f'Ошибка VK #{e.error_code}: {e.error_msg}')
        return redirect('/')

    if method == "edit_responses":#--------------------------------------------------------------
        for key in db.responses.keys():
            response = request.form.get(key)
            if response: db.responses[key] = response
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
        temp = {'name': request.form['new_name'],
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
        return redirect('/admin')

    return int_error('Тебя здесь быть не должно')


def db_check_user(request):  # TODO: убрать
    uid = auth['user']
    if uid == 0:
        return redirect('/login'), 'fail'
    try:
        return DB(int(uid)), 'ok'
    except ExcDB as e:
        if e.code == 0:
            return int_error('В админ панель можно зайти только с аккаунта дежурного 💅🏻'), 'fail'
        else:
            return int_error(e), 'fail'


@app.route('/admin')
def admin():
    db_gen = DB_general()
    if DEBUG:
        db = DB()
    else:
        db, response = db_check_user(request)
        if response != 'ok':
            return db

    warning = 0

    login = login_check(request, db, db_gen)
    if login:
        return login

    users = VkApi(db.access_token)('users.get', fields='photo_50',
                                   user_ids=db.duty_id)
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


@app.errorhandler(ExcDB)
def db_error(e: ExcDB):
    logger.error(f'Ошибка при обработке запроса:\n{traceback.format_exc()}')
    if e.code == 0 and auth['user'] == 0:
        return redirect('/login')
    return int_error(e.text)


@app.errorhandler(Exception)
def on_error(e: Exception):
    logger.error(f'Ошибка при обработке запроса:\n' +
                 traceback.format_exc())
    return f'Неизвестная ошибка:\n{e.__class__.__name__}: {e}'


@app.errorhandler(json.decoder.JSONDecodeError)
def decode_error(e):
    logger.error(f'Ошибка при декодировании данных:\n{e}\n{traceback.format_exc()}')  # noqa
    return f'Произошла ошибка при декодировании данных, проверьте файлы в ICAD/database<br>Место, где споткнулся декодер: {e}'  # noqa
