import requests, json, re
from ..sync import sync_send
from .utils import send_info, ExcReload, msg_op
from microvk import VkApi

def service_commands(nd, db, vk: VkApi):
    if nd[5] == '!syncchanges':
        data = json.loads(sync_send('get_unsynced', {}, db))
        db.__dict__.update(data)
        response = sync_send('sync_ok', {}, db)
        if response == 'ok':
            db.save()
            raise ExcReload(db.gen.group_id)
        else:
            send_info(f'Ошибка синхронизации. Ответ сервера:\n{response}')
            
    elif nd[5].startswith('!связать шабы'):
        pid = re.findall(r'(\[id)?(\d+)', nd[5])
        if pid:
            if pid[0][0]:
                pid = int(pid[0][1])
            elif pid[0][1]:
                pid = int(pid[0][1]) + 2000000000
        else:
            pid = nd[3]
        db.settings['templates_bind'] = pid
        db.save()
        msg_op(3, nd[3], msg_id = nd[1])

    elif nd[5] == '!отвязать шабы':
        db.settings['templates_bind'] = 0
        db.save()
        msg_op(3, nd[3], msg_id = nd[1])

    elif nd[5] == '!чаты':
        chats = ''
        for chat in vk(vk.messages.getConversations, count = 200)['items']:
            chat = chat['conversation']
            if chat['peer']['type'] == 'chat':
                chats += f"{chat['chat_settings']['title']}\nID: {chat['peer']['id'] - 2000000000}\n\n"
            if len(chats) > 1000:
                break
        msg_op(1, nd[3], chats)

    elif nd[5] == '!лпстоп':
        raise Exception('forcestop')

    elif nd[5] == '!лпрестарт':
        raise ExcReload(nd[3])
    return "ok"