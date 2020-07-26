# да, я знаю, что здесь код получился особенно отбитым
# потом переделаю
from .utils import msg_op, parseByID, att_parse, parse
from . import dlp, ND
from ..objects import DB
from ..sync import tmp_sync
from microvk import VkApi
import time, requests, io
from animstarter import start_player
from typing import List, Any


def player(pic: list, delay: float, nd: List[Any], vk):
        for i in range(len(pic)):
            msg_op(2, nd[3], f'{pic[i]}', nd[1], keep_forward_messages = 1, api = vk)
            time.sleep(delay)


def tmp_op(mode, db, data = {}, tmp_type = ''):# mode: 0 - список, 1 - получение, 2 - запись, 3 - удаление
    # tmp_type = 'dyn' - операции с динамическими шаблонами
    temps = getattr(db, tmp_type + 'templates')

    def tmp_cycle(mode = mode):
        i = 0
        message = ''
        for temp in temps:
            if mode == 0:
                i += 1
                if tmp_type == 'dyn':
                    add = f"| Скорость: {temp['speed']}"
                else:
                    add = f"| {temp['cat']}"
                message += f"\n{i}. {temp['name']} {add}"
            else:
                if temp['name'].lower() == data['name'].lower():
                    if mode == 1: return temp
                    else:
                        temps.remove(temp)
                        return db.save()
        return message
    if mode == 2:
        tmp_cycle(3)
        temps.append(data)
        return db.save()
    else: return tmp_cycle()


@dlp.register_startswith('шабы', 'шаб', '+шаб', '-шаб')
def template(nd: ND):
    msg = nd.msg

    category = 'без категории'

    try:
        msg['args'].remove('') # костыли на костылях, но переделывать это в нормальный код я уже не буду
    except:
        pass

    spl = " ".join(msg['args']).split('|')
    if len(spl) > 1: category = spl[1]
    if category.lower() == 'все': category = 'без категории'
    name = spl[0].strip()

    if msg['command'] == 'шабы':
        if 'все' in msg['args']:
            message = 'Список всех шаблонов:' + tmp_op(0, nd.db)
        else:
            message = "Категории шаблонов:"
            cats = set()
            i = 1
            temps = nd.db.templates
            for temp in temps:
                if temp['cat'] not in cats:
                    message += f"\n{i}. {temp['cat']}"
                    cats.add(temp['cat'])
                    i += 1
            if msg['args']:
                cat = ' '.join(msg['args'])
                if cat in cats:
                    i = 1
                    message = f'''Шаблоны категории "{cat}":'''
                    for temp in temps:
                        if temp['cat'] == cat.lower():
                            message += f"\n{i}. {temp['name']}"
                            i += 1

        
    
        msg_op(2, nd[3], message, nd[1])
        return "ok"


    if len(msg['args']) == 0:
            msg_op(2, nd[3], "❗ Нет данных", msg_id = nd[1])


    if msg['command'] == '+шаб':
        if ((msg['payload'] == '') and len(msg['attachments']) == 0 
        and nd[7].get('reply') == None):
            msg_op(2, nd[3], "❗ Нет данных", msg_id = nd[1])
            return "ok"

        if msg['reply']:
            data = msg['reply']['text']
            for att in msg['reply']['attachments']:
                if att.get('type') == 'audio_message':
                    att = att['audio_message']
                    audio_url = att['link_mp3']
                    response = requests.get(url = audio_url)
                    audio_msg = io.BytesIO(response.content)
                    upload_url = nd.vk('docs.getUploadServer',
                        type = 'audio_message')['upload_url']
                    uploaded = requests.post(upload_url, files = {'file': audio_msg}).json()['file']
                    audio = nd.vk('docs.save', file = uploaded)['audio_message']
                    att.update({"owner_id": audio['owner_id'],
                    "id": audio['id'],"access_key": audio['access_key']})
                    del(audio_msg)
            msg['attachments'] = att_parse(msg['reply']['attachments'])
        else: data = msg['payload']
        tmp = {"name": name,"payload": data,"cat": category.strip(),
            "attachments": msg['attachments']}
        tmp_op(2, nd.db, tmp)

        msg['text'] = f'✅ Шаблон "{name}" сохранен.'
        if nd.db.gen.mode == 'LP-CB':
            if tmp_sync(2, tmp, nd.db) == "ok":
                msg['text'] += '\n☑️ Успешно синхронизировано'
            else:
                msg['text'] += '\n⚠️ Ошибка синхронизации'

        msg_op(2, nd[3], msg['text'], msg_id = nd[1], delete = 1)
        return "ok"


    if msg['command'] == '-шаб':
        if tmp_op(3, nd.db, {'name':name}):
            msg = f'✅Шаблон "{name}" удален.'
            if nd.db.gen.mode == 'LP-CB':
                if tmp_sync(3, {'name': name}, nd.db) == "ok":
                    msg += '\n☑️ Успешно синхронизировано'
                else: msg+= '\n⚠️ Ошибка синхронизации'
            msg_op(2, nd[3], msg, nd[1], delete = 1)
            return "ok"


    if msg['command'] == 'шаб':
        temp = tmp_op(1, nd.db, {'name':name})
        if temp:
            bind = nd.db.settings['templates_bind']
            msg['id'] = msg['reply']['id'] if msg['reply'] else []
            if not temp['payload']: temp['payload'] = msg['payload']
            temp['attachments'].extend(nd.msg['attachments'])
            atts = ",".join(temp['attachments'])
            if atts.startswith('audio_message'):
                nd.vk('execute', code = """API.messages.send({"peer_id":%d,"message":"%s",
                "attachment":"%s","reply_to":"%s","random_id":0});
                API.messages.delete({"message_ids":%d,"delete_for_all":1});""" %
                (nd[3], nd.msg['payload'].replace('\n', '<br>'), atts,
                nd.msg['reply']['id'] if nd.msg['reply'] else '', nd[1]))
            else:
                msg_op(2, bind if bind else nd[3], temp['payload'], keep_forward_messages = 1,
                    attachment=atts, msg_id = nd[1])
            temp['payload'] = ''
            return "ok"


    msg_op(2, nd[3], f'❗ Шаблон "{name}" не найден.', nd[1], delete = 1)
    return "ok"


@dlp.register_startswith('анимк', '+анимка', '-анимка')
def dyntemplate(nd: ND):
    msg = nd.msg

    try:
        msg['args'].remove('') # костыли на костылях, но переделывать это в нормальный код я уже не буду
    except:
        pass

    name = " ".join(msg['args'])
    if 'скорость' in msg['args']:
        spd = float(msg['args'][msg['args'].index('скорость') + 1])
        name = name.replace(f' скорость {spd}', '')
    else: spd = 1


    if msg['command'] == 'анимки' or msg['command'] == 'мои':
        if msg['args']:
            if msg['args'][0] != 'анимки':
                return "ok"
        message = "Ваши анимки:"
        message += tmp_op(0, nd.db, tmp_type = 'dyn')
        if message == "Ваши анимки:":
            message = "У вас нет ни одной анимки :("
        msg_op(2, nd[3], message, nd[1])
        return "ok"


    if len(msg['args']) == 0:
            msg_op(2, nd[3], "❗ Нет данных", msg_id = nd[1])


    if msg['command'] == '+анимка':
        if ((msg['payload'] == '') and len(msg['attachments']) == 0 
        and nd[7].get('reply') == None):
            msg_op(2, nd[3], "❗ Нет данных", msg_id = nd[1])
            return "ok"

        tmp_op(2, nd.db, {"name": name,"speed": spd, "frames": msg['payload'].split('#$')}, 'dyn')

        msg['text'] = (f'✅ Анимка "{name}" сохранена\n' +
        '(здесь очень кривая реализация, лучше пользуйтесь сайтом)')

        msg_op(2, nd[3], msg['text'], msg_id = nd[1], disable_mentions = 1)
        return "ok"


    if msg['command'] == '-анимка':    
        if tmp_op(3, nd.db, {'name':name}, 'dyn'):
            msg_op(2, nd[3], f'✅ Анимка "{name}" удалена', nd[1])
            return "ok"


    if msg['command'] == 'анимка':
        temp = tmp_op(1, nd.db, {'name':name}, 'dyn')
        start_player(nd[3], nd[1], nd.db.access_token, temp['frames'], temp['speed'], True)
        return "ok"


    msg_op(2, nd[3], f'❗ Шаблон "{name}" не найден.', nd[1])
    return "ok"


    

