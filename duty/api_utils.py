from microvk import VkApi, VkApiResponseException
from typing import List,Union
import requests


def get_last_th_msgs(peer_id: int, api: VkApi) -> List[dict]:
    return api.exe('''return (API.messages.getHistory({"peer_id":"%(peer)s",
    "count":"200", "offset":0}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":200}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":400}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":600}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":800}).items);''' % {'peer': peer_id})


def get_msgs(peer_id, api: VkApi, offset = 0):
    return api.exe('''return (API.messages.getHistory({"peer_id":"%s",
    "count":"200", "offset":"%s"}).items) + (API.messages.getHistory({"peer_id":
    "%s", "count":"200", "offset":"%s"}).items);''' %
    (peer_id, offset, peer_id, offset + 200))


def set_online_privacy(db, mode = 'only_me'):
    url = ('https://api.vk.com/method/account.setPrivacy?v=5.109&key=online&value=%s&access_token=%s'
    % (mode, db.me_token))
    r = requests.get(url, headers = {"user-agent": "VKAndroidApp/1.123-123 (Android 123; SDK 123; IrCA; 1; ru; 123x123)"}).json()
    if r['response']['category'] == mode:
        return True
    else:
        return False


def get_msg(vk: VkApi, peer_id: int, local_id: int) -> Union[dict, None]:
    try:
        return vk(
            "messages.getByConversationMessageId",
            conversation_message_ids=local_id, peer_id=peer_id
        )['items'][0]
    except (KeyError, IndexError):
        return None


def get_msg_id(vk: VkApi, peer_id: int, local_id: int) -> Union[int, None]:
    msg = get_msg(vk, peer_id, local_id)
    return msg['id'] if msg else None
