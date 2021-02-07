from vkapi import VkApi, VkApiResponseException
import typing
import time
import re


def get_all_history_gen(vk: VkApi, chat_id: int, offset: int = 0) -> typing.Generator[dict, None, None]:
    chat = vk("messages.getHistory", count=1, peer_id=chat_id, offset=offset)
    count = chat['count']
    while offset < count:
        try:
            chat = vk(
                "messages.getHistory",
                count=200,
                peer_id=chat_id,
                offset=offset
            )
        except (Exception, VkApiResponseException):
            time.sleep(3)
            continue

        offset += 200
        for item in chat['items']:
            yield item


def get_msg_id(vk: VkApi, chat_id: int, local_id: int) -> typing.Union[int, None]:
    try:
        data = vk("messages.getByConversationMessageId", peer_id=chat_id, conversation_message_ids=local_id)
        return data['items'][0]['id']
    except (Exception, VkApiResponseException):
        return None


def get_msg(vk: VkApi, chat_id: int, local_id: int) -> typing.Union[dict, None]:
    try:
        data = vk("messages.getByConversationMessageId", peer_id=chat_id, conversation_message_ids=local_id)
        if len(data['items']) != 0:
            return data['items'][0]
        return None
    except (Exception, VkApiResponseException):
        return None


def get_msg_ids(vk: VkApi, chat_id: int, local_ids: list) -> typing.Generator[int, None, list]:
    try:
        local_ids = [str(li) for li in local_ids]
        data = vk("messages.getByConversationMessageId", peer_id=chat_id, conversation_message_ids=",".join(local_ids))
        for item in data['items']:
            yield item['id']
    except (Exception, VkApiResponseException):
        return []


def search_user_id(s: str) -> typing.Union[int, None]:
    regexp = r"id([\d]+)"
    data = re.findall(regexp, s)
    if len(data) == 0:
        return None

    return int(data[0])


def search_group_id(s: str) -> typing.Union[int, None]:
    regexp = r"club([\d]+)"
    data = re.findall(regexp, s)
    if len(data) == 0:
        return None
    return int(data[0])


def edit_message(api: VkApi, chat_id: int, msg_id: int, **kwargs) -> int:
    return api("messages.edit", peer_id=chat_id, message_id=msg_id, **kwargs)


def new_message(api: VkApi, chat_id: int, **kwargs) -> int:
    return api("messages.send", random_id=0, peer_id=chat_id, **kwargs)
