from microvk import VkApi
import typing


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


def ment_user(user):
    return f"[id{user['id']}|{user['first_name']} {user['last_name']}]"


def edit_message(api: VkApi, chat_id: int, msg_id: int, **kwargs) -> int:
    return api("messages.edit", peer_id=chat_id, message_id=msg_id, **kwargs)


def delete_message(api: VkApi, chat_id: int, msg_id: int, **kwargs) -> int:
    return api("messages.delete", peer_id=chat_id, message_id=msg_id, delete_for_all=True, **kwargs) 


def new_message(api: VkApi, chat_id: int, **kwargs) -> int:
    return api("messages.send", random_id=0, peer_id=chat_id, **kwargs)


def sticker_message(api: VkApi, chat_id: int, sticker_id: int, **kwargs) -> int:
    return api("messages.send", random_id=0, peer_id=chat_id, sticker_id=sticker_id, **kwargs)

