import requests
from . import VkApi
from datetime import datetime

from logger import get_writer
logger = get_writer('VK LongPoll')

class LP():
    key: str
    server:str
    ts: int
    time: float
    vk: VkApi
    wait: int

    def __init__(self, vk, wait = 25):
        'vk - экземпляр VkApi'
        self.vk = vk
        data = vk('messages.getLongPollServer')
        if data.get('error'):
            if data['error']['error_code'] == 5:
                raise Exception('tokenfail')
        self.server = data['server']
        self.key = data['key']
        self.ts = data['ts']
        self.wait = wait

    @property
    def check(self):
        'Возвращает список событий (updates)'
        response = requests.get(f"http://{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait={self.wait}&version=3&mode=2")

        if response.status_code != 200:
            logger.error('Ошибка сети')
            return []

        self.time = datetime.now().timestamp()
        data = response.json()

        if 'failed' in data.keys():
            if data['failed'] == 1:
                logger.error('Ошибка истории событий')
                self.ts = data['ts']
            elif data['failed'] == 2:
                self.key = self.vk('messages.getLongPollServer')['key']
            else:
                raise Exception('Информация о пользователе утрачена')
            return []
        else:
            self.ts = data['ts']
            return data['updates']
