import json
import re

from flask import Request

from microvk import VkApi

from datetime import datetime

from .. import utils
from ..lpcommands.utils import utils_api
from . import DB

from wtflog import warden
logger = warden.get_boy(__name__)


class ExceptToJson(Exception):
    response: str

    def __init__(self, message, code = '', mode = ''):
        if mode == 'iris':
            self.response = json.dumps({'response': 'error',
            'error_code': code, 'error_message': message}, ensure_ascii = False)
        else:
            self.response = 'Error_o4ka:\n' + str(message)


class Chat:
    id: int
    peer_id: int
    iris_id: str
    name: str

    def __init__(self, data: dict, iris_id: str):
        self.peer_id = data.get('peer_id', 0)
        self.id = self.peer_id - 2000000000
        self.name = data.get('name', '')
        self.iris_id = iris_id
        self.installed = data.get('installed', False)


class Event:
    db: DB
    method: str

    api: VkApi

    msg: dict

    time: float
    vk_response_time: float
    obj: dict
    fails: dict
    secret: str
    chat: Chat
    attachments: list
    reply_message: dict
    responses: dict

    def set_msg(self):
        ct = datetime.now().timestamp()
        self.msg = utils.get_msg(
            self.api, self.chat.peer_id, self.msg['conversation_message_id'])
        self.vk_response_time = datetime.now().timestamp() - ct
        self.parse_attachments()
        self.reply_message = self.msg.get("reply_message", None)

    def set_chat(self):
        if 'chat' not in self.obj.keys():
            return
        if self.obj['chat'] in self.db.chats.keys():
            self.chat = Chat(
                self.db.chats[self.obj['chat']], self.obj['chat'])
            if self.msg != (None, {}):
                self.set_msg()
            return

        if self.msg not in [None, {}]:
            chats = self.api("messages.getConversations",
                             count=100, filter="all")
            for item in chats['items']:
                conver = item['conversation']
                if conver['peer']['type'] == "chat":
                    message = utils.get_msg(
                        self.api, conver['peer']['id'], self.msg['conversation_message_id'])
                    if message == None:
                        continue
                    if message['from_id'] == self.msg['from_id'] and message['date'] == self.msg['date']:
                        self.db.chats.update(
                            {
                                self.obj['chat']: {
                                    "peer_id": conver['peer']['id'],
                                    "name": conver['chat_settings']['title'],
                                    "installed": False
                                }
                            }
                        )
                        self.chat = Chat(self.db.chats[self.obj['chat']], self.obj['chat'])
                        
                        self.db.save()
                        self.set_msg()
                        break
            return
        self.chat = None

    def __init__(self, request: Request, data_: dict=None):

        if request != None and request.data == b'':
            self.user_id = None
            self.msg = None
            self.obj = None
            self.secret = None
            self.method = 'ping'
        else:
            if data_ == None:
                _data = json.loads(request.data)
            else:
                _data = data_
            self.secret = _data.get('secret')
            self.obj = _data.get('object', {})
            self.msg = _data.get('message', {})

            try:
                self.db = DB(_data.get('user_id'))
            except:
                raise ExceptToJson('Неверный ID дежурного')

            self.time = datetime.now().timestamp()
            self.api = VkApi(self.db.access_token, raise_excepts=True)
            self.method = _data.get('method', 'ping')
            self.attachments = []
            self.responses = self.db.responses

            utils_api(self.db, self.api)

            if self.method in {'sendSignal', 'sendMySignal', 'subscribeSignals', 'toGroup'}:
                self.set_chat()
            elif self.method in {'ping', 'groupbots.invited', 'bindChat'}:
                pass
            else:
                self.chat = Chat(self.db.chats[self.obj['chat']], self.obj['chat'])


        logger.info(self.__str__().replace('\n', ' '))

    def parse_attachments(self):
        for attachment in self.msg.get('attachments', []):
            a_type = attachment['type']
            if a_type in ['link']:
                continue
            self.attachments.append(
                f"{a_type}{attachment[a_type]['owner_id']}_{attachment[a_type]['id']}_{attachment[a_type]['access_key']}"
            )

    def __str__(self) -> str:
        return f"""Новое событие от Iris callback API
            Метод: {self.method}
            Пользователь: {self.db.duty_id}
            Данные: {json.dumps(self.obj, ensure_ascii=False)}
            Сообщение: {json.dumps(self.msg, ensure_ascii=False)}
            """.replace("    ", "")


class SignalEvent(Event):
    msg: dict
    chat: Chat

    time: float
    vk_response_time: float
    command: str
    args: list
    payload: str

    reply_message: dict

    def __str__(self) -> str:
        return f"""Новое событие от Iris callback API
            Метод: {self.method}
            Команда: {self.command}
            Агрументы: {self.args}
            Пользователь: {self.db.duty_id}
            Данные: {json.dumps(self.obj, ensure_ascii=False)}
            Сообщение: {json.dumps(self.msg, ensure_ascii=False)}
            """.replace("    ", "")

    def parse(self):
        regexp = r"(^[\S]+)|([\S]+)|(\n[\s\S \n]+)"
        _args = re.findall(regexp, self.msg['text'])
        args = []
        payload = ""

        for arg in _args:
            if arg[1] != '':
                args.append(arg[1])
            if arg[2] != '':
                payload = arg[2][1:]

        if len(args) == 1:
            self.command = args[0].lower()
            self.args = None
        else:
            self.command = args[0].lower()
            self.args = args[1:]

        self.payload = payload

    def __init__(self, event: Event):
        self.event = event
        self.time = event.time
        self.vk_response_time = event.vk_response_time
        self.api = event.api
        self.db = event.db
        self.method = event.method
        self.obj = event.obj
        self.secret = event.secret
        self.attachments = event.attachments
        self.chat = event.chat
        self.msg = event.msg
        self.reply_message = event.reply_message
        self.responses = event.responses

        self.parse()
        logger.debug(self.__str__().replace('\n', ' '))


class MySignalEvent(Event):

    msg: dict
    chat: Chat

    time: float
    vk_response_time: float
    command: str
    args: list
    payload: str

    reply_message: dict

    def __init__(self, event: Event):
        self.event = event
        self.api = event.api
        self.time = event.time
        self.vk_response_time = event.vk_response_time
        self.db = event.db
        self.method = event.method
        self.obj = event.obj
        self.secret = event.secret
        self.attachments = event.attachments
        self.chat = event.chat
        self.msg = event.msg
        self.reply_message = event.reply_message
        self.responses = event.responses

        self.parse()
        logger.debug(self.__str__().replace('\n', ' '))

    def parse(self):
        regexp = r"(^[\S]+)|([\S]+)|(\n[\s\S \n]+)"
        _args = re.findall(regexp, self.msg['text'])
        args = []
        payload = ""

        for arg in _args:
            if arg[1] != '':
                args.append(arg[1])
            if arg[2] != '':
                payload = arg[2][1:]

        if len(args) == 1:
            self.command = args[0].lower()
            self.args = None
        else:
            self.command = args[0].lower()
            self.args = args[1:]

        self.payload = payload

    def msg_op(self, mode, text = '', **kwargs):
        '1 - новое сообщение, 2 - редактирование, 3 - удаление для всех'
        msg_id = self.msg['id'] if mode in {2, 3, 4} else 0
        self.api.msg_op(mode, self.chat.peer_id, text, msg_id, **kwargs)