import io
import re
import time
import requests
from html import escape
from typing import Any, List, Tuple, Union

from idm.objects import MySignalEvent, dp
from .template import delete_template



@dp.my_signal_event_register('+гс')
def voice_create(event: MySignalEvent) -> str:
    name = re.findall(r"([^|]+)\|?([^|]*)", ' '.join(event.args))
    if not name:
        event.msg_op(2, "❗ Не указано название")
        return "ok"
    category = name[0][1].lower().strip() or 'без категории'
    name = name[0][0].lower().strip()

    if category == 'все':
        event.msg_op(2, '❗ Невозможно создать голосовое сообщение ' +
                     'с категорией "все"')
        return "ok"

    try:
        if event.reply_message['attachments'][0]['type'] != 'audio_message':
            raise TypeError
    except (KeyError, IndexError, TypeError):
        event.msg_op(2, "❗ Необходим ответ на голосовое сообщение")
        return "ok"

    attach = event.reply_message['attachments'][0]['audio_message']
    data = requests.get(attach['link_mp3'])
    audio_msg = io.BytesIO(data.content)
    audio_msg.name = 'voice.mp3'
    upload_url = event.api('docs.getUploadServer',
                           type='audio_message')['upload_url']
    uploaded = requests.post(upload_url,
                             files={'file': audio_msg}).json()['file']
    audio = event.api('docs.save', file=uploaded)['audio_message']
    del(audio_msg)
    voice = f"audio_message{audio['owner_id']}_{audio['id']}_{audio['access_key']}"

    event.db.voices, exist = delete_template(name, event.db.voices)
    event.db.voices.append({
        "name": name,
        "cat": category,
        "attachments": voice
    })
    event.db.save()

    event.msg_op(2, f'✅ Голосовое сообщение "{name}" ' +
                 ('перезаписано' if exist else 'сохранено') +
                 f'\nДлительность - {attach["duration"]} сек.')
    return "ok"


@dp.my_signal_event_register('гсы')
def template_list(event: MySignalEvent) -> str:
    category = ' '.join(event.args)
    voices = event.db.voices
    if category == 'все':
        message = '📃 Список всех голосовых сообщений:'
        for i, v in enumerate(voices, 1):
            message += f"\n{i}. {v['name']} | {v['cat']}"
    elif not category:
        cats = {}
        for v in voices:
            cats[v['cat']] = cats.get(v['cat'], 0) + 1
        message = "📚 Категории голосовых сообщений:"
        for cat in cats:
            message += f"\n-- {cat} ({cats[cat]})"
    else:
        message = f'📖 Голосовые сообщения категории "{category}":'
        for v in voices:
            if v['cat'] == category:
                message += f"\n-- {v['name']}"
    if not '\n' in message:
        message = '⚠️ Голосовые сообщения по указанному запросу не найдены'
    event.msg_op(2, message)
    return "ok"


@dp.my_signal_event_register('-гс')
def voice_delete(event: MySignalEvent) -> str:
    name = ' '.join(event.args).lower()
    event.db.voices, exist = delete_template(name, event.db.voices)
    if exist:
        msg = f'✅ Голосовое сообщение "{name}" удалено'
        event.db.save()
    else:
        msg = f'⚠️ Голосовое сообщение "{name}" не найдено'
    event.msg_op(2, msg, delete = 2)
    return "ok"


@dp.my_signal_event_register('гс')
def voice_send(event: MySignalEvent) -> str:
    name = ' '.join(event.args).lower()
    voice = None
    for v in event.db.anim:
        if v['name'] == name:
            voice = v
            break
    if voice:
        reply = str(event.reply_message['id']) if event.reply_message else ''
        event.api.exe(
            'API.messages.delete({' +
            '"message_ids":'+str(event.msg['id'])+',"delete_for_all":1});' +
            'API.messages.send({'
                '"peer_id":%d,' % event.chat.peer_id +
                '"message":"%s",' % escape(event.payload).replace('\n', '<br>') +
                '"attachment":"%s",' % voice['attachments'][0] +
                '"reply_to":"%s",' % reply +
                '"random_id":0});')
    else:
        event.msg_op(2, f'❗ Голосовое сообщение "{name}" не найдено')
    return "ok"
