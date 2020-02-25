from ...objects import dp, MySignalEvent, DB
from vkapi import VkApi
import time
import typing

from ...utils import new_message

from enum import Enum

class Frame:
    time: float
    data: str

    def __init__(self, **kwargs):
        self.time = kwargs.get('time', 3)
        self.data = kwargs.get('data', 'Потерянный фрейм')

    def render(self, api: VkApi, peer_id: int, message_id: int) -> int:
        try:
            s = api("messages.edit", peer_id=peer_id, message_id=message_id, message=self.data)
            time.sleep(self.time)
            return s
        except:
            time.sleep(self.time)
            return 0

        


""" 
🌕🌕🌗🌑🌑🌑🌑🌑🌓
🌕🌕🌗🌑🌑🌑🌑🌑🌕
🌕🌕🌗🌑🌓🌕🌕🌕🌕
🌕🌕🌗🌑🌓🌕🌕🌕🌕
🌕🌕🌗🌑🌑🌑🌑🌓🌕
🌕🌕🌗🌑🌑🌑🌑🌕🌕
🌕🌕🌗🌑🌓🌕🌕🌕🌕
🌕🌕🌗🌑🌓🌕🌕🌕🌕
🌕🌕🌗🌑🌓🌕🌕🌕🌕
"""

class DynamicTemplateType(Enum):
    LTOR = "ltor"
    RTOL = "rtol"
    BY_PERSONNEL = "by_personnel"



class DynamicTemplate:

    """ 
        Если тип by_personnel кадры { time, data }
        Если тип LTOR или RTOL шаблон { type, time, data, name }
    """

    frames: typing.List[Frame]
    type: str
    raw: dict
    name: str

    time: float
    data: str

    def __init__(self, db: DB, name: str):
        self.frames = []

        for data in db.dynamic_templates:
            if data['name'] == name:
                self.raw = data

        self.type = DynamicTemplateType(self.raw.get('type', "by_personnel"))

        if self.type == DynamicTemplateType.BY_PERSONNEL:
            for fr in self.raw['frames']:
                self.frames.append(Frame(**fr))
        elif self.type == DynamicTemplateType.LTOR:
            self.time = self.raw.get('time', 3)
            _data_split = self.raw['data'].split('\n')
            for _ in range(0, len(_data_split[0]) + 1 ):
                self.frames.append(Frame(time=self.time, data="\n".join(_data_split)))
                __data_split = [
                    d[-1] + d[:-1]
                    for d in _data_split
                ]
                _data_split = __data_split
        elif self.type == DynamicTemplateType.RTOL:
            self.time = self.raw.get('time', 3)
            _data_split = self.raw['data'].split('\n')
            for _ in range(0, len(_data_split[0]) + 1 ):
                self.frames.append(Frame(time=self.time, data="\n".join(_data_split)))
                __data_split = [
                    d[1:] + d[0] 
                    for d in _data_split
                ]
                _data_split = __data_split



    def run(self, api: VkApi, peer_id: int, message_id: int):
        fr = []
        for frame in self.frames:
            d = frame.render(api, peer_id, message_id)
            fr.append(d)
        return fr

@dp.my_signal_event_handle('дшаб')
def dtemplate(event: MySignalEvent) -> str:
    
    name = event.args[0]

    dt = DynamicTemplate(event.db, name)
    d = dt.run(event.api, event.chat.peer_id, event.msg['id'])

    new_message(event.api, event.chat.peer_id, message=f"Рендер шаблона окончен\n Фреймов: {len(dt.frames)}\nОтчет: {d}")
    return "ok"