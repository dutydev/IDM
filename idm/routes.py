# я тоже ничего разобрать в этой каше не могу, ты не одинок
from flask import (Flask, redirect, request, render_template,
    send_from_directory, abort)
from .objects import Event, dp, DB, ExcDB, ExceptToJson, DB_general
from .lpcommands.utils import gen_secret, set_online_privacy
from .sync import lpsync, secret_fail_lp
from microvk import VkApi
from hashlib import md5
from wtflog import warden
import json, requests, re, time, traceback

app = Flask(__name__)

logger = warden.get_boy(__name__)

def reload():
    import uwsgi
    uwsgi.reload()
    pass


def get_mask(token:str) -> str:
        if len(token) != 85: return 'Не установлен'
        return token[:4] + "*" * 77 + token[81:]


def login_check(request, db: DB, db_gen: DB_general, check_owner = False):
    uid = db.duty_id
    token = request.cookies.get('token')
    if not db_gen.installed:
        return redirect('/install')
    if not uid or uid != db.duty_id:
        return redirect('/login?next=/admin')
    if md5(f"{db_gen.vk_app_id}{uid}{db_gen.vk_app_secret}".encode()).hexdigest() != token:
        return redirect('/login?next=/admin')
    if check_owner and uid != db_gen.owner_id:
        return abort(403)


def format_tokens(tokens: list):
    for i in range(len(tokens)):
        token = re.search(r'access_token=[a-z0-9]{85}', tokens[i])
        if token: token = token[0][13:]
        elif len(tokens[i]) == 85: token = tokens[i]
        else: token = None
        tokens[i] = token
    return tokens


def check_tokens(tokens:list):
    user_ids = []
    for i in range(len(tokens)):
        try:
            user_ids.append(VkApi(tokens[i])('users.get')[0]['id'])
            time.sleep(0.4)
        except:
            return int_error("Неверный токен, попробуйте снова")
    return user_ids

def lp_installed(db_gen):
    return int_error(f'''(нет, не ошибка)<br>Установка прошла успешно<br>
            <br>Теперь управление модулем осуществляется через
            <a href="{db_gen.host}">{db_gen.host}</a><br>
            <br>Этот сайт больше недоступен'''.replace('    ', ''))

@app.route('/')
def index():
    db = DB_general()
    if db.installed: return redirect('/admin')
    return redirect('/install')



@app.route('/reload')
def reload_page():
    reload()
    return 'ok'



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

    if method == 'sync':
        return lpsync(request)

    db_gen = DB_general()

    if method == "setup_cb":#--------------------------------------------------------------
        if db_gen.installed: return redirect('/')
        
        tokens = format_tokens([request.form.get('access_token'), request.form.get('me_token')])
        
        user_id = check_tokens(tokens)[0]
        if type(user_id) != int: return user_id

        db_gen.add_user(user_id, True)
        db = DB(user_id)

        db.access_token = tokens[0]
        db.me_token = tokens[1]
        
        db.secret = gen_secret()
        db_gen.vk_app_id = int(request.form.get('vk_app_id'))
        db_gen.vk_app_secret = request.form.get('vk_app_secret')
        db_gen.host = "http://" + request.host
        db_gen.installed = True
        db.trusted_users.append(db.duty_id)
        if request.form.get('lp'):
            db_gen.mode = 'LP'
        else:
            db_gen.mode = 'CB'
        db.save()
        db_gen.save()
        if db_gen.mode == 'LP':
            return int_error(f'''(нет, не ошибка)<br>Установка прошла успешно
            <br>Этот сайт больше недоступен'''.replace('    ', ''))
        return redirect('/login?next=/admin')


    if method == 'setup_lp':#--------------------------------------------------------------
        if request.data:
            jdata = json.loads(request.data)
            db = DB(jdata['user_id'])
            fail = secret_fail_lp(jdata, db)
            if fail:
                return fail
            db.lp['installed'] = True
            db.save()
            return json.dumps({"token": db.lp_token,
            "me_token": db.me_token, "host": db_gen.host})
        else:
            if db_gen.installed:
                return redirect('/')
            url = 'http://' + re.search(r'(\w*\.)?\w*\.\w*',
            request.form.get('url'))[0]
            if url == 'http://' + request.host:
                return int_error('Вы должны указать адрес сайта ранее установленного дежурного')
            uid = int(request.form.get('user_id'))
            r = requests.post(url + '/api/setup_lp',
            data = json.dumps({"secret": request.form.get('secret'),
            "user_id": uid})).text
            if r == 'Неверное секретное слово': return int_error(r)
            try:
                jdata = json.loads(r)
            except:
                return int_error('Неверный адрес или дежурный не настроен')
            db_gen.add_user(uid, True)

            db = DB(uid)
            db.access_token = jdata['token']
            db.me_token = jdata['me_token']
            db.secret = request.form.get('secret')
            db.save()
            
            db_gen.host = jdata['host']
            db_gen.installed = True
            db_gen.mode = 'LP-CB'
            db_gen.save()
            reload()
            return int_error(f'''(нет, не ошибка)<br>Установка прошла успешно<br>
            <br>Теперь управление модулем осуществляется через
            <a href="{db_gen.host}">{db_gen.host}</a><br>
            <br>Этот сайт больше недоступен'''.replace('    ', ''))

    db = DB(request.cookies.get('uid'))

    login = login_check(request, db, db_gen)
    if login: return login


    if method == 'edit_lp':#oco6a9l ]|[ona, Da, 9I 3Hal-0
        form = request.form
        sets = db.settings

        if form['farm'] == 'off':
            sets['farm']['on'] = sets['farm']['soft'] = False
        else:
            sets['farm']['on'] = True
            if form['farm'] == 'soft': sets['farm']['soft'] = True
        
        if form['lp_token']:
            db.lp_token = format_tokens([form['lp_token']])[0]
        if form['prefix']: sets['prefix'] = form['prefix'] + ' '

        if form['del_requests'] == 'on': sets['del_requests'] = True
        else: sets['del_requests'] = False

        if form['friends_add'] == 'on': sets['friends_add'] = True
        else: sets['friends_add'] = False

        if form['online'] == 'on' and sets['online'] == False:
            sets['online'] = True
        else: sets['online'] = False

        if form['offline'] == 'on':
            if sets['online']: sets['online'] = False
            set_online_privacy(db)
            sets['offline'] = True
        elif sets['offline']:
            set_online_privacy(db, 'all')
            sets['offline'] = False

        db_orig = DB(request.cookies.get('uid'))
        if db_orig.settings != db.settings:
            db.lp['unsynced_changes'].update({'settings': db.settings})

        db.save()
        VkApi(db.access_token).msg_op(1, -195759899, '!syncchanges')
        return redirect('/')

    if method == "edit_current_user":#--------------------------------------------------------------
        tokens = format_tokens([request.form.get('access_token', ''),
            request.form.get('me_token', ''), request.form.get('lp_token', '')])
        if tokens[0]: db.access_token = tokens[0]
        if tokens[1]: db.me_token = tokens[1]
        if tokens[2]: db.lp_token = tokens[2]
        db.save()
        return redirect('/admin')


    if method == 'connect_to_iris':
        uid = request.form.get('id')
        if uid: db = DB(int(uid))
        try:
            VkApi(db.access_token, raise_excepts = True)('messages.send', random_id = 0,
                message = f'+api {db.secret} {db.gen.host}/callback', peer_id = -174105461)
        except:
            return int_error('Что-то пошло не так :/')
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
        for i in range(len(db.dyntemplates)):
            if db.dyntemplates[i]['name'] == name:
                db.dyntemplates[i].update(temp)
                break
        db.save()
        return redirect('/admin#DynTemplates')


    if method == 'add_dyntemplate':
        db.dyntemplates.append({'name': 'анимка',
            'frames': ['Отсутствует'], 'speed': 1.0})
        db.save()
        return redirect('/admin#DynTemplates')

    if method == 'delete_anim':
        name = request.form['name']
        for i in range(len(db.dyntemplates)):
            if db.dyntemplates[i]['name'] == name:
                del(db.dyntemplates[i])
                db.save()
                return redirect('/admin#DynTemplates')

    return int_error('Тебя здесь быть не должно')



@app.route('/admin/edit_user', methods = ["POST"])
def edit_user():
    return abort(403)



def db_check_user(request):
    uid = request.cookies.get('uid')
    if not uid: return redirect('/login'), 'fail'
    try:
        return DB(int(uid)), 'ok'
    except ExcDB as e:
        if e.code == 0: return int_error('В админ панель можно зайти только с аккаунта дежурного 💅🏻'), 'fail'
        else: return int_error(e), 'fail'



@app.route('/admin')
def admin():
    db_gen = DB_general()
    db, response = db_check_user(request)
    if response != 'ok': return db

    warning = 0

    login = login_check(request, db, db_gen)
    if login: return login

    if db.duty_id == db.full_db['owner_id']:
        user_list = db_gen.users
        owner = True
    else:
        user_list = [db.duty_id]
        owner = False

    users = VkApi(db.access_token)('users.get', fields = 'photo_50',
        user_ids = ','.join(str(u) for u in user_list))
    if type(users) == dict:
        username = 'unknown'
        warning = {'type':'danger', 'text':'Ошибка доступа, смени токены'}
    else:
        username = f"{users[0]['first_name']} {users[0]['last_name']}"
    

    db.access_token = get_mask(db.access_token)
    db.me_token = get_mask(db.me_token)

    return render_template('pages/admin.html', db = db, users = users, owner = owner,
        farm = db.settings['farm'], prefix = db.settings['prefix'].replace(' ', ''),
        warn = warning, username = username)


@app.route('/login')
def login():
    db = DB_general()
    return render_template('pages/login.html', vk_app_id = db.vk_app_id)



@app.route('/callback', methods=["POST"])
def callback():
    event = Event(request)

    secret = event.secret

    if secret != event.db.secret:
        fails = event.fails
        if secret != fails['last']:
            fails['count'] += 1
            fails['last'] = secret
            event.db.gen.save()
        return 'Неверная секретка', 500

    d = dp.event_run(event)
    if d == "ok":
        return json.dumps({"response":"ok"}, ensure_ascii = False)
    elif type(d) == dict:
        return json.dumps(d, ensure_ascii = False)
    else:
        return r"\\\\\ашипка хэз бин произошла/////" + '\n' + d


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def int_error(e):
    return render_template('errors/500.html', error = e), 500

@app.errorhandler(ExceptToJson)
def json_error(e):
    return e.response

@app.errorhandler(ExcDB)
def db_error(e):
    return int_error(e.text)

@app.errorhandler(Exception)
def on_error(e):
    logger.error(f'Ошибка при обработке запроса:\n{e}\n{traceback.format_exc()}')
    return f'Неизвестная ошибка:\n{e}'