from .objects import DB, DB_general
from flask import request
from .lpcommands.utils import msg_op
import json, requests, time
from microvk import VkApi
from hashlib import md5
from wtflog import warden

logger = warden.get_boy('Модуль синхронизации')


def tmp_op_sync(mode, data = {}, db = 0, tmp_type = ''):# mode: 2 - запись, 3 - удаление
    pass


def secret_fail_lp(jdata, db: DB_general):
    secret = jdata['secret']
    if secret != db.secret:
        return 'Неверное секретное слово', 500



def lpsync(request):
    pass


def sync_send(type, data, db):
    pass


def tmp_sync(mode, data, db):
    pass


def token_request():
    pass