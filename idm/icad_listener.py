import json
import requests
import traceback

from flask import request
from typing import Union

from idm import app
from idm.objects import DB, db_gen, Chat
from idm.utils import Message
from idm.my_signals.remote import set_session, DC

from microvk import VkApi, VkApiResponseException
from wtflog import warden

logger = warden.get_boy('Модуль удаленного управления')

session: Union[str, None]


def register():
    global session
    r = requests.post(DC, json={
        'method': 'register',
        'user_id': str(db_gen.owner_id),
        'token': DB().access_token if db_gen.dc_auth else None,
        'host': db_gen.host
    }, timeout=3)
    if r.status_code == 200:
        session = set_session(r.json()['response'])


if db_gen.installed:
    try:
        register()
    except Exception:
        session = None


class error:
    HostTroubles = 1
    NotTrusted = 2
    WrongSession = 3
    NotBinded = 4
    VkError = 5

    @staticmethod
    def json(name):
        return json.dumps({'error': getattr(error, name)})


@app.route('/remote', methods=["POST"])
def handle_rc():
    if session is None:
        return error.json('HostTroubles')

    data = json.loads(request.data)
    db = DB()

    if data['user_id'] not in db.trusted_users:
        return error.json('NotTrusted')
    if data['session'] != session:
        return error.json('WrongSession')
    if data['chat'] not in db.chats:
        return error.json('NotBinded')

    try:
        send(db, data)
    except VkApiResponseException as e:
        return {'error': error.VkError, 'code': e.error_code, 'msg': e.error_msg}
    except Exception:
        logger.error("Ошибка при обработке запроса. Данные: " +
                     json.dumps(data, indent=2) + '\n' +
                     traceback.format_exc())
        return error.json('HostTroubles')
    return "ok"


def send(db: DB, data: dict):
    chat = Chat(db.chats[data['chat']], data['chat'])
    vk = VkApi(db.access_token, raise_excepts=True)

    msg = vk("messages.getByConversationMessageId",
             conversation_message_ids=data['local_id'],
             peer_id=chat.peer_id)['items'][0]
    msg = Message(msg)

    if msg.reply:
        replies = {'reply_to': msg.reply['id']}
    elif msg.fwd:
        replies = {'forward_messages': ','.join(
            [str(fwd['id']) for fwd in msg.fwd]
        )}
    else:
        replies = {}

    vk.msg_op(1, chat.peer_id, msg.payload, **replies,
              attachment=','.join(msg.attachments))
