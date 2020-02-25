from .objects import DB
from vkapi import VkApi, VkApiResponseException
import json
from flask import render_template
import typing
import time
import re

def get_all_history_gen(vk: VkApi, chat_id: int) -> typing.Generator[dict, None, None]:
    __offset = 0
    chat = vk("messages.getHistory", count=1, peer_id=chat_id, offset=__offset)
    count = chat['count']
    while __offset < count:
        chat = {}

        try:
            
            chat = vk("messages.getHistory", count=200,
                        peer_id=chat_id, offset=__offset)
            time.sleep(1)        
        except:
            time.sleep(3)            
            continue

        __offset += 200 
        for item in chat['items']:
            yield item

def get_msg_id(vk: VkApi, chat_id: int, local_id: int) -> typing.Union[int, None]:
    try:
        data = vk("messages.getByConversationMessageId", peer_id=chat_id, conversation_message_ids=local_id)
        return data['items'][0]['id']
    except:
        return None

def get_msg(vk: VkApi, chat_id: int, local_id: int)-> typing.Union[dict, None]:
    try:
        data = vk("messages.getByConversationMessageId", peer_id=chat_id, conversation_message_ids=local_id)
        if len(data['items']) != 0:
            return data['items'][0]
        return None
    except:
        return None

def get_msg_ids(vk: VkApi, chat_id: int, local_ids: list) -> typing.Generator[int, None, list]:
    try:
        local_ids = [str(li) for li in local_ids]
        data = vk("messages.getByConversationMessageId", peer_id=chat_id, conversation_message_ids=",".join(local_ids))
        for item in data['items']:
            yield item['id']
    except:
        return []

def search_user_id(s: str) -> typing.Union[int, None]:
    regexp = r"id([\d]+)"
    data = re.findall(regexp, s)
    if len(data) == 0:return None
    else:return int(data[0])

def search_group_id(s: str) -> typing.Union[int, None]:
    regexp = r"club([\d]+)"
    data = re.findall(regexp, s)
    if len(data) == 0:return None
    else:return int(data[0])

def edit_message(api: VkApi, chat_id: int, msg_id: int, **kwargs) -> int:
    return api("messages.edit", peer_id=chat_id, message_id=msg_id, **kwargs)

def new_message(api: VkApi, chat_id: int, **kwargs) -> int:
    return api("messages.send", random_id=0, peer_id=chat_id, **kwargs)