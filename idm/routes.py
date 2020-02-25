from flask import Flask, redirect, request, render_template
from .objects import Event, dp, DB
import typing
from vkapi import VkApi, VkApiResponseException
from hashlib import md5
import traceback

import json

app = Flask(__name__)

@app.route('/')
def index():
    db = DB()
    return render_template('pages/index.html', installed=db.installed)

@app.route('/install')
def install():
    db = DB()
    return render_template('pages/install.html', installed=db.installed)

@app.route('/api/<string:method>', methods=["POST"])
def api(method: str):
   
    db = DB()

    if method == "setup_idm":
        if db.installed: return redirect('/')
        local_db = DB()
        local_db.owner_id = int(request.form.get('owner_id', None))
        local_db.secret = request.form.get('secret', None)
        local_db.access_token = request.form.get('access_token', None)

        local_db.online_token = request.form.get('online_token', None) if request.form.get('online_token', None) != '' else None
        local_db.me_token = request.form.get('me_token', None) if request.form.get('me_token', None) != '' else None
        local_db.bp_token = request.form.get('bp_token', None) if request.form.get('bp_token', None) != '' else None

        local_db.vk_app_id = int(request.form.get('vk_app_id', None))
        local_db.vk_app_secret = request.form.get('vk_app_secret', None)
        local_db.host = request.form.get('host', None)
        local_db.installed = True
        local_db.trusted_users.append(local_db.owner_id)
        local_db.duty_id = VkApi(local_db.access_token)('users.get')[0]['id']
        local_db.trusted_users.append(local_db.duty_id)
        
        
        db = local_db
        db.save()
        return redirect('/login?next=/')   

    if method == "edit_bot":
        
        if request.form.get('uid', None) == None:
            return redirect('/login?next=/admin')
        uid = int(request.form.get('uid', None))
        token = request.form.get('token', None)
        if uid != db.owner_id and uid != db.duty_id:
            return redirect('/')
        if md5(f"{db.vk_app_id}{uid}{db.vk_app_secret}".encode()).hexdigest() != token:
            return redirect('/login?next=/admin')
        
        db.secret = request.form.get('secret', None)

        access_token = request.form.get('access_token', None)
        online_token = request.form.get('online_token', None)
        bp_token = request.form.get('bp_token', None)
        me_token = request.form.get('me_token', None)

        if access_token != None and access_token != '' and '*' not in access_token:
            db.access_token = access_token
        if online_token != None and online_token != '' and '*' not in online_token:
            db.online_token = online_token
        if bp_token != None and bp_token != '' and '*' not in bp_token:
            db.bp_token = bp_token
        if me_token != None and me_token != '' and '*' not in me_token:
            db.me_token = me_token
        db.save()
        return redirect('/admin')      

    if method == "reset":
        secret = request.form.get('secret', None)
        if secret == db.secret:
            db.installed = False
            db.chats = {}
            db.trusted_users = []
            db.owner_id = 0
            db.duty_id = 0
            db.vk_app_id = 0
            db.vk_app_secret = ""
            db.host = ""
            db.secret = ""
            db.access_token = None
            db.online_token = None
            db.me_token = None
            db.bp_token = None
            db.save()
        return redirect('/')

    return "ok"

@app.route('/admin')
def admin():
    def get_musk(token:str) -> str:
        if token == None or len(token) != 85:return ""
        return token[:4] + "*" * 77 + token[81:]


    db = DB()
    uid = request.cookies.get('uid', 0)
    token = request.cookies.get('token', None)
    if not db.installed:
        return redirect('/install')
    if request.cookies.get('uid', None) == None:
        return redirect('/login?next=/admin')
    if int(request.cookies.get('uid', 0)) != db.owner_id and int(request.cookies.get('uid', 0)) != db.duty_id:
        return redirect('/')
    if md5(f"{db.vk_app_id}{uid}{db.vk_app_secret}".encode()).hexdigest() != token:
        return redirect('/login?next=/admin')
    
    local_db = db

    local_db.access_token = get_musk(db.access_token)
    local_db.me_token = get_musk(db.me_token)
    local_db.online_token = get_musk(db.online_token)
    local_db.bp_token = get_musk(db.bp_token)

    return render_template('pages/admin.html', db=local_db.raw)

@app.route('/login')
def login():
    db = DB()
    return render_template('pages/login.html', vk_app_id=db.vk_app_id)

@app.route('/callback', methods=["POST"])
def callback():
    event = Event(request)
    if event.db.secret != event.secret:
        return "Неверный секретный код"
    if event.user_id != event.db.duty_id:
        return "Неверный ID дежурного"
    data = [d for d in dp.event_run(event)]
    for d in data:
        if d != "ok":
            return "<ошибочка>" + json.dumps({"ошибка":d}, ensure_ascii=False, indent=2)
    return "ok"


@app.errorhandler(Exception)
def on_error(e):
    return "<ошибочка>" + json.dumps({"тип":"неизвесный (on_error)", "ошибка":f"{e}"}, ensure_ascii=False, indent=2)
     