import json
import requests
import traceback

from flask import request, jsonify, send_from_directory
from typing import Union

from duty import app
from duty.objects import Chat, db, __version__
from duty.utils import Message

from microvk import VkApi, VkApiResponseException
from logger import get_writer

logger = get_writer('Модуль удаленного управления')


if db.installed:
    try:
        VkApi(db.access_token).exe('''API.messages.delete({
            "message_ids": API.messages.send({
                "peer_id":-195759899, "message":"%s", "random_id": 0
            }),
            "delete_for_all": 1
        });''' % f'+cod {db.secret} {db.host}/')
    except Exception:
        db.dc_secret = None


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
    db.dc_secret = data['dc_secret']
    db.sync()
    return 'ok'


@app.route('/chex', methods=["POST"])
def chex():
    data = json.loads(request.data)
    if data['dc_secret'] != db.dc_secret:
        return jsonify(error='WrongSecret')

    try:
        user_id = VkApi(db.access_token, True)('users.get')[0]['id']
        me_id = VkApi(db.me_token, True)('users.get')[0]['id']
    except VkApiResponseException:
        pass

    return jsonify(
        owner_id=db.owner_id,
        user_id=locals().get('user_id', 0),
        me_id=locals().get('me_id', 0),
        mt=(1 if 'me_id' in locals() else 0),
        v=__version__
    )


@app.route('/log', methods=["GET"])
def remote_log():
    data = json.loads(request.data)
    if data['dc_secret'] != db.dc_secret:
        return jsonify(error='WrongSecret')
    else:
        return send_from_directory(join(dirname(dirname(dirname(__file__))), f"duty.log"))
    


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
