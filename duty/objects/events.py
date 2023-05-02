import json
from datetime import datetime
from typing import Dict, List, Union

from flask import Request

from logger import get_writer
from microvk import VkApi

from .database import db
from duty.utils import Message, cmid_key
from duty.api_utils import get_msg

logger = get_writer('События callback')


class ExceptToJson(Exception):
    response: str

    def __init__(self, message='', code: int = 0, iris: bool = False):
        if iris:
            self.response = json.dumps({
                    'response': 'error',
                    'error_code': code,
                    'error_message': message
                }, ensure_ascii=False)
        else:
            self.response = 'Error_o4ka:\n' + str(message)


class Chat:
    id: int
    name: str
    peer_id: int
    iris_id: str
    installed: bool

    def __init__(self, data: dict, iris_id: str):
        self.peer_id = data['peer_id']
        self.id = self.peer_id - 2000000000
        self.name = data.get('name', 'Чат не связан')
        self.iris_id = iris_id
        self.installed = data.get('installed', False)


class Event:
    db = db
    method: str

    api: VkApi

    msg: dict

    time: float
    vk_response_time: float
    obj: dict
    secret: str
    chat: Union[Chat, None]
    reply_message: dict
    responses: dict

    def set_msg(self, msg: 'dict | None' = None):
        if msg is None:
            ct = datetime.now().timestamp()
            self.msg = get_msg(self.api, self.chat.peer_id, self.msg[cmid_key])
            self.vk_response_time = datetime.now().timestamp() - ct
        else:
            self.msg = msg
        self.parse()

    def set_chat(self):
        if 'chat' not in self.obj.keys():
            raise ValueError('В событии отсутствует ID чата!')

        if self.obj['chat'] in self.db.chats.keys():
            self.chat = Chat(self.db.chats[self.obj['chat']], self.obj['chat'])
            return

        if not self.msg:
            raise RuntimeError('Невозможно связать чат! '
                               'В событии отсутствует сообщение!')

        if self.msg[cmid_key] is None:
            raise ExceptToJson(code=10, iris=True)

        ct = datetime.now().timestamp()
        search_res = self.api("messages.search",
                              q=self.msg['text'], count=10, extended=1)
        self.vk_response_time = datetime.now().timestamp() - ct

        message = None
        for msg in search_res['items']:
            if msg[cmid_key] == self.msg[cmid_key]:
                if msg['from_id'] == self.msg['from_id']:
                    message = msg
                    break
        if message is None:
            raise RuntimeError('Не могу привязать чат! '
                               'Не нашёл сообщение-команду')

        for conv in search_res['conversations']:
            if conv['peer']['id'] == message['peer_id']:
                chat_name = conv['chat_settings']['title']
                break

        chat_raw = {
            "peer_id": message['peer_id'],
            "name": chat_name,  # type: ignore
            "installed": False
        }
        self.db.chats.update({self.obj['chat']: chat_raw})
        self.chat = Chat(chat_raw, self.obj['chat'])
        self.set_msg(message)


    def __init__(self, request: Request):
        if request.data == b'':
            self.user_id = None
            self.msg = None
            self.obj = None
            self.secret = None
            self.method = 'ping'
        else:
            _data = json.loads(request.data)
            self.secret = _data.get('secret')
            self.obj = _data.get('object', {})
            self.msg = _data.get('message', {})

            if int(_data.get('user_id')) != db.owner_id:
                raise ExceptToJson('Неверный ID дежурного')

            self.time = datetime.now().timestamp()
            self.api = VkApi(self.db.access_token, raise_excepts=True)
            self.method = _data.get('method', 'ping')
            self.responses = self.db.responses

            if self.method in {'sendSignal', 'sendMySignal',
                               'subscribeSignals', 'toGroup'}:
                self.set_chat()
            elif self.method in {'ping', 'groupbots.invited',
                                 'bindChat', 'meetChatDuty'}:
                pass
            else:
                chat = self.obj['chat']
                if chat not in self.db.chats:
                    raise ExceptToJson(f'Чат #{chat} не связан!')
                self.chat = Chat(self.db.chats[chat], chat)
        if self.method not in {'sendSignal', 'sendMySignal'}:
            logger.info(self.__str__())

    def send(self, text='', **kwargs) -> int:
        if self.chat is None:
            raise RuntimeError(
                'Невозможно отправить соообщение, т.к. чат не установлен'
            )
        return self.api.msg_op(1, self.chat.peer_id, text, **kwargs)

    def edit_msg(self, message_id: int, text='', **kwargs):
        if self.chat is None:
            raise RuntimeError(
                'Невозможно отредактировать соообщение, т.к. чат не установлен'
            )
        return self.api.msg_op(2, self.chat.peer_id, text, message_id, **kwargs)

    def parse(self):
        msg = Message(self.msg)
        self.reply_message = self.msg.get("reply_message", None)
        self.attachments = msg.attachments
        self.command = msg.command
        self.payload = msg.payload
        self.args = msg.args

    def __str__(self) -> str:
        obj_ = self.obj
        return f"""Новое событие от Iris callback API
            Метод: {self.method}
            Данные: {obj_}
            Сообщение: {self.msg}
            """.replace("    ", "")


class SignalEvent(Event):
    command: str
    args: list
    payload: str
    attachments: List[str]

    def __init__(self, event: Event):
        self.time = event.time
        self.api = event.api
        self.db = event.db
        self.method = event.method
        self.obj = event.obj
        self.msg = event.msg
        self.secret = event.secret
        self.chat = event.chat
        self.responses = event.responses

        logger.debug(self.__str__())


class MySignalEvent(Event):
    command: str
    args: List[str]
    payload: str
    attachments: List[str]

    def __init__(self, event: Event):
        self.api = event.api
        self.time = event.time
        self.db = event.db
        self.method = event.method
        self.obj = event.obj
        self.msg = event.msg
        self.secret = event.secret
        self.chat = event.chat
        self.responses = event.responses

        logger.debug(self.__str__())

    def msg_op(self, mode, text:str='', **kwargs):
        '1 - новое сообщение, 2 - редактирование, 3 - удаление для всех'
        msg_id = self.msg['id'] if mode in {2, 3, 4} else 0
        self.api.msg_op(mode, self.chat.peer_id, text.replace('&amp;', '&').replace('&quot;', '&').replace('&lt;', '<').replace('&gt;', '>'), msg_id, **kwargs)

    def send(self, message: str = '', **params) -> int:
        'Отправка в чат, из которого пришло событие, нового сообщения'
        return self.msg_op(1, message, **params)

    def edit(self, message: str = '', **params) -> int:
        'Редактирование сообщения-события'
        return self.msg_op(2, message, **params)

    def delete(self) -> Dict[str, int]:
        'Удаление сообщения-события'
        return self.msg_op(3)


class LongpollEvent(MySignalEvent):
    method = 'Longpoll'
    data: dict

    def __str__(self) -> str:
        return f"""Новое событие от Longpoll модуля
            Команда: {self.command}
            Аргументы: {self.args}
            Данные: {self.data}
            Сообщение: {self.msg}
            """.replace("    ", "")

    def __init__(self, data: dict):
        self.time = datetime.now().timestamp()
        self.data = data
        self.msg = data['message']
        self.parse()
        self.command = data.get('command', self.command)
        if data['chat'] is None:
            self.chat = Chat({'peer_id': self.msg['peer_id']}, 'N/A')
        else:
            self.chat = Chat(self.db.chats[data['chat']], data['chat'])
        self.api = VkApi(self.db.access_token, raise_excepts=True)
        self.responses = self.db.responses

        logger.debug(self.__str__())
