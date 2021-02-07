from typing import Union, Iterable

from ..objects import dp, Event, utils
from ..utils import get_all_history_gen

OK = {'response': 'ok'}


def join(data: Union[str, Iterable], separator: str = ",") -> str:
    if isinstance(data, str):
        data = [data]
    if not data:
        return ''
    return separator.join([str(obj) for obj in data])


def forwarded_checker(message: dict) -> bool:
    return True if message.get('fwd_messages') else False


def wall_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'wall' in attach:
            return True
    return False


def stickers_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'sticker' in attach:
            return True
    return False


def voice_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'audio_message' in attach:
            return True
    return False


def gif_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'doc' in attach and attach['doc']['ext'] == 'gif':
            return True
    return False


def photo_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'photo' in attach:
            return True
    return False


def video_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'video' in attach:
            return True
    return False


def audio_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'audio' in attach:
            return True
    return False


def article_checker(message: dict) -> bool:
    for attach in message['attachments']:
        if 'link' in attach and 'vk.com/@' in attach['link']['url']:
            return True
    return False


def any_checker(message: dict) -> bool:
    return True


def period_checker(message: dict) -> bool:
    return True


CHECKERS = {
    "forwarded": forwarded_checker,
    "wall": wall_checker,
    "stickers": stickers_checker,
    "voice": voice_checker,
    "gif": gif_checker,
    "photo": photo_checker,
    "video": video_checker,
    "audio": audio_checker,
    "article": article_checker,
    "any": any_checker,
    "period": period_checker
}


@dp.event_handle(dp.Methods.DELETE_MESSAGES_BY_TYPE)
def delete_messages_by_type(event: Event) -> Union[str, dict]:
    message_id = utils.new_message(event.api, event.chat.peer_id, message="... удаляю сообщения ...")
    now = event.api.method('utils.getServerTime')
    message_ids = []
    deleted_message_ids = []

    for message in get_all_history_gen(event.api, event.chat.peer_id, offset=event.obj['offset']):
        if event.obj['amount']:
            if len(message_ids) + len(deleted_message_ids) == event.obj['amount']:
                break
        if message['date'] < now - 86400:
            break

        if isinstance(event.obj['admin_ids'], list):
            if message['from_id'] in event.obj['admin_ids']:
                continue
        else:
            if str(message['from_id']) in event.obj['admin_ids']:
                continue
        if CHECKERS[event.obj['type']](message):
            message_ids.append(message['id'])
        if len(message_ids) % 200 == 0 and len(message_ids):
            try:
                event.api.method(
                    'messages.delete',
                    message_ids=join(message_ids),
                    delete_for_all=1,
                    spam=event.obj.get('is_spam', 0)
                )
            finally:
                deleted_message_ids.extend(message_ids)
                message_ids = []

    if message_ids:
        try:
            event.api.method(
                'messages.delete',
                message_ids=join(message_ids),
                delete_for_all=1,
                spam=event.obj.get('is_spam', 0)
            )
        finally:
            deleted_message_ids.extend(message_ids)
            message_ids = []
    utils.edit_message(event.api, event.chat.peer_id, message_id, message="✅ Сообщения удалены")

    return {'response': 'ok'}
