
import requests
from . import VkApi



class Longpoll(object):

    def __init__(self, api: VkApi, group_id: int, wait: int = 25):
        self.api = api
        self.group_id = group_id
        self.wait = 25
        data = self.api("groups.getLongPollServer", group_id=self.group_id)

        self.key = data['key']
        self.server = data['server']
        self.ts = data['ts']

    def check(self):
        data = requests.get(f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait={self.wait}")
        if data.status_code != 200:
            raise Exception("Network error")

        djson = data.json()

        if 'failed' in djson.keys():
            if djson['failed'] == 1:
                self.ts = djson['ts']
            else:
                data = self.api("groups.getLongPollServer", group_id=self.group_id)
                self.key = data['key']
                self.server = data['server']
                self.ts = data['ts']
            return {"ts": self.ts, "updates": []}

        else:
            self.ts = djson['ts']
            return djson

    
    def listen(self):
        while True:
            yield self.check()
