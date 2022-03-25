import json
import requests
import traceback

from flask import request, jsonify
from typing import Union

from duty import app
from duty.objects import Chat, db
from duty.utils import Message
from duty.my_signals.remote import set_session, DC

from microvk import VkApi, VkApiResponseException
from logger import get_writer

logger = get_writer('Модуль удаленного управления')

session: Union[str, None]


if db.installed:
    try:
        VkApi(db.access_token).msg_op(1, group_dc, f'+cod {db.secret} {db.host}/')
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


@app.route('/dc', methods=["POST"])
def get_dc_secret():
    data = json.loads(request.data)
    if data['user_id'] != db.owner_id:
        return jsonify({'error': 'NotMe'})
    if data['secret'] != db.secret:
        return jsonify({'error': 'WrongSecret'})
    _ = db.dc_secret  # не ебу надо это или нет, но до пизды, все равно один раз ставится
    db.dc_secret = data['dc_secret']
    db.sync()
    return 'ok'


@app.route('/chex', methods=["POST"])
def chex():
    data = json.loads(request.data)
    print(data['dc_secret'], db.dc_secret)
    if data['dc_secret'] != db.dc_secret:
        return jsonify(error='WrongSecret')
    user_id = 0
    try:
        user_id = VkApi(db.access_token, raise_excepts=True)('users.get')[0]['id']
    except VkApiResponseException:
        pass

    me_id = 0
    mt = 0
    try:
        me_id = VkApi(db.me_token, raise_excepts=True)('users.get')[0]['id']
    except VkApiResponseException:
        mt = 1 if db.access_token != '' else 0

    return jsonify(owner_id=db.owner_id, user_id=user_id, me_id=me_id, mt=mt)


@app.route('/remote', methods=["POST"])
def handle_rc():
    data = json.loads(request.data)
    if data['user_id'] not in db.trusted_users:
        return error.json('NotTrusted')
    if data['secret'] != db.dc_secret:
        return error.json('WrongSecret')
    if data['chat'] not in db.chats:
        return error.json('NotBinded')

    try:
        ok = send(data)
        if not ok:
            return error.json('NotTrusted')
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
    if data['user_id'] != msg['from_id']:
        return 0
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
    return 1
