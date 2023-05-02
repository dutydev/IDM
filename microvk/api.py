from typing import Any

import requests

from logger import get_writer

from .methods import Messages

logger = get_writer('VK API')


class VkApiResponseException(Exception):
    def __init__(self, *args, **kwargs):
        self.error_code = kwargs.get('error_code', None)
        self.error_msg = kwargs.get('error_msg', None)
        self.request_params = kwargs.get('request_params', None)

        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return 'Ошибка #%s: "%s"' % (self.error_code, self.error_msg)


class VkApi:
    url: str = 'https://api.vk.com/method/'
    query: str
    raise_excepts: bool

    messages = Messages

    def __init__(self, access_token: str, raise_excepts: bool = False, version: str = "5.110"):
        'raise_excepts - если True, ошибки ВК будут вызывать исключения'
        self.query = f'?v={version}&access_token={access_token}&lang=ru'
        self.raise_excepts = raise_excepts

    def __call__(self, method, **kwargs) -> Any:
        logger.debug(f'URL = "{self.url}{method}{self.query}" Data = {kwargs}')
        r = requests.post(f'{self.url}{method}{self.query}', data=kwargs)
        if r.status_code == 200:
            r = r.json()
            if 'response' in r.keys():
                logger.info(f"Запрос {method} выполнен")
                return r['response']
            elif 'error' in r.keys():
                logger.warning(f"Запрос {method} не выполнен: {r['error']}")
                if self.raise_excepts:
                    raise VkApiResponseException(**r["error"])
            return r
        elif self.raise_excepts:
            raise Exception('networkerror')

    def method(self, method, **kwargs):
        return self.__call__(method, **kwargs)

    def message_send(self, message: str, peer_id: int, **kwargs):
        return self.msg_op(1, peer_id, message, **kwargs)

    def msg_op(self, mode: int, peer_id: int = 0, message = '', msg_id = '', **kwargs):
        '''mode: 1 - отправка, 2 - редактирование, 3 - удаление, 4 - удаление только для себя'''

        if mode == 4:
            mode = 3
            dfa = 0
        else: dfa = 1

        method = ['messages.send', 'messages.edit', 'messages.delete'][mode - 1]

        return self(
            method,
            peer_id=peer_id,
            message=message,
            message_id=msg_id,
            delete_for_all=dfa,
            random_id=0,
            **kwargs
        )

    def exe(self, code, token: 'str | None' = None):
        if token:
            return VkApi(token)('execute', code = code)
        return self('execute', code = code)
