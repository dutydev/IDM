import json
import re

from flask import Request

from vkapi import VkApi

from .. import utils
from . import DB, Methods

import logging
logger = logging.getLogger(__name__)


class Chat:
    id: int
    peer_id: int
    iris_id: str
    name: str

    def __init__(self, data: dict, iris_id: str, installed: bool):
        self.peer_id = data.get('peer_id', 0)
        self.id = self.peer_id - 2000000000
        self.name = data.get('name', '')
        self.iris_id = iris_id
        self.installed = data.get('installed', False)


class Event:
    db: DB
    method: Methods

    api: VkApi

    msg: dict
    message: dict

    obj: dict
    object: dict

    user_id: str
    secret: str
    chat: Chat
    attachments: list
    reply_message: dict

    def set_msg(self):
        self.message = self.msg = utils.get_msg(
            self.api, self.chat.peer_id, self.msg['conversation_message_id'])
        self.parse_attachments()
        self.reply_message = self.msg.get("reply_message", None)

    def set_chat(self):
        if 'chat' not in self.obj.keys():
            return
        if self.obj['chat'] in self.db.chats.keys():
            self.chat = Chat(
                self.db.chats[self.obj['chat']], self.obj['chat'], self.obj['chat'])
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
                        self.db.save()
                        self.set_msg()
                        break
            return
        self.chat = None

    def __init__(self, request: Request, data_: dict=None):

        if request != None and request.data == b'':
            self.user_id = None
            self.message = self.msg = None
            self.object = self.obj = None
            self.secret = None
            self.method = Methods.PING
        else:
            if data_ == None:
                _data = json.loads(request.data)
            else:
                _data = data_
            self.user_id = _data.get('user_id', None)
            self.secret = _data.get('secret', None)
            self.object = self.obj = _data.get('object', {})
            self.message = self.msg = _data.get('message', {})

            self.db = DB()
            self.api = VkApi(self.db.access_token, raise_excepts=True)
            self.method = Methods(_data.get('method', 'ping'))
            self.attachments = []

            if self.method in [Methods.BIND_CHAT, Methods.SEND_SIGNAL, Methods.SEND_MY_SIGNAL, Methods.SUBSCRIBE_SIGNALS, Methods.TO_GROUP]:
                self.set_chat()
            elif self.method == Methods.PING:
                pass
            else:
                self.chat = Chat(
                    self.db.chats[self.obj['chat']], self.obj['chat'], self.obj['chat'])

                self.message = self.msg = None
                self.reply_message = None


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
            Пользователь: {self.user_id}
            Данные: {json.dumps(self.object, ensure_ascii=False)}
            Сообщение: {json.dumps(self.message, ensure_ascii=False)}
            """.replace("    ", "")


class SignalEvent(Event):
    message: dict
    msg: dict
    chat: Chat

    command: str
    args: list
    payload: str

    reply_message: dict

    def __str__(self) -> str:
        return f"""Новое событие от Iris callback API
            Метод: {self.method}
            Команда: {self.command}
            Агрументы: {self.args}
            Пользователь: {self.user_id}
            Данные: {json.dumps(self.object, ensure_ascii=False)}
            Сообщение: {json.dumps(self.message, ensure_ascii=False)}
            """.replace("    ", "")

    def parse(self):
        regexp = r"(^[\S]+)|([\S]+)|(\n[\s\S \n]+)"
        _args = re.findall(regexp, self.message['text'])
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
        self.api = event.api
        self.db = event.db
        self.method = event.method
        self.obj = event.obj
        self.object = event.object
        self.user_id = event.user_id
        self.secret = event.secret
        self.attachments = event.attachments
        self.chat = event.chat
        self.message = event.message
        self.msg = event.msg
        self.reply_message = event.reply_message

        self.parse()
        logger.debug(self.__str__().replace('\n', ' '))


class MySignalEvent(Event):

    message: dict
    msg: dict
    chat: Chat

    command: str
    args: list
    payload: str

    reply_message: dict

    def __init__(self, event: Event):
        self.event = event
        self.api = event.api
        self.db = event.db
        self.method = event.method
        self.obj = event.obj
        self.object = event.object
        self.user_id = event.user_id
        self.secret = event.secret
        self.attachments = event.attachments
        self.chat = event.chat
        self.message = event.message
        self.msg = event.msg
        self.reply_message = event.reply_message

        self.parse()
        logger.debug(self.__str__().replace('\n', ' '))

    def parse(self):
        regexp = r"(^[\S]+)|([\S]+)|(\n[\s\S \n]+)"
        _args = re.findall(regexp, self.message['text'])
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
