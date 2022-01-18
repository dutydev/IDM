import json
import requests
import traceback

from flask import request
from typing import Union

from duty import app
from duty.objects import Chat, db
from duty.utils import Message
from duty.my_signals.remote import set_session, DC

from microvk import VkApi, VkApiResponseException
from logger import get_writer

logger = get_writer('Модуль удаленного управления')

session: Union[str, None]


def register():
    global session
    r = requests.post(DC, json={
        'method': 'register',
        'user_id': str(db.owner_id),
        'token': db.access_token if db.dc_auth else None,
        'host': db.host
    }, timeout=3)
    if r.status_code == 200:
        session = set_session(r.json()['response'])


if db.installed:
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

    if data['user_id'] not in db.trusted_users:
        return error.json('NotTrusted')
    if data['session'] != session:
        return error.json('WrongSession')
    if data['chat'] not in db.chats:
        return error.json('NotBinded')

    try:
        send(data)
    except VkApiResponseException as e:
        return {'error': error.VkError, 'code': e.error_code, 'msg': e.error_msg}
    except Exception:
        logger.error("Ошибка при обработке запроса. Данные: " +
                     json.dumps(data, indent=2) + '\n' +
                     traceback.format_exc())
        return error.json('HostTroubles')
    return "ok"


def send(data: dict):
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
