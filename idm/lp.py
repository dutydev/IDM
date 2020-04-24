from vkapi import VkApi, Longpoll
from .objects import DB
db = DB()
def execme(code: str) -> int:
    if db.me_token == '':
        return "-1"
    vk = VkApi(access_token = db.me_token)
    vk.method('execute', code = code)
    return "ok"

def executetest(code: str) -> int:
    yourway = VkApi(access_token = db.access_token)
    meme = yourway.method('execute', code = code)
    return meme

def IIS(message: str):
    vk = VkApi(access_token = db.access_token)
    vk.method('messages.send', user_id = 332619272,
    random_id = 0, message = message)