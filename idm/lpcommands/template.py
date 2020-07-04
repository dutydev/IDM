# да, я знаю, что здесь код получился особенно отбитым
# потом переделаю
from .utils import msg_op, parseByID, att_parse, parse
from . import dlp, ND
from ..objects import DB
from ..sync import tmp_sync
from microvk import VkApi
import time, requests, io


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
            msg_op(2, bind if bind else nd[3], temp['payload'], keep_forward_messages = 1,
                attachment=",".join(temp['attachments'], msg_id = nd[1]))
            temp['payload'] = ''
            return "ok"


    msg_op(2, nd[3], f'❗ Шаблон "{name}" не найден.', nd[1], delete = 1)
    return "ok"


@dlp.register_startswith('анимк', '+анимка', '-анимка')
def dyntemplate(nd: ND):
    msg = nd.msg

    name = " ".join(msg['args'])
    if 'скорость' in msg['args']:
        spd = float(msg['args'][msg['args'].index('скорость') + 1])
        name = name.replace(f' скорость {spd}', '')
    else: spd = 1


    if msg['command'] == 'анимки' or msg['command'] == 'мои':
        if msg['args']:
            if msg['args'][0] != 'анимки':
                return "ok"
        message = "Ваши динамические шаблоны:"
        message += tmp_op(0, nd.db, tmp_type = 'dyn')
    
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

        msg['text'] = (f'✅ Динамический шаблон "{name}" сохранен.'
        '(здесь очень кривая реализация, лучше пользуйтесь сайтом)')

        msg_op(2, nd[3], msg['text'], msg_id = nd[1], disable_mentions = 1)
        return "ok"


    if msg['command'] == '-анимка':    
        if tmp_op(3, nd.db, {'name':name}, 'dyn'):
            msg_op(2, nd[3], f'✅ Динамический шаблон "{name}" удален.', nd[1])
            return "ok"


    if msg['command'] == 'анимка':
        temp = tmp_op(1, nd.db, {'name':name}, 'dyn')
        for frame in temp['frames']:
            msg_op(2, nd[3], frame, nd[1], keep_forward_messages = 1)
            time.sleep(temp['speed'])
        return "ok"


    msg_op(2, nd[3], f'❗ Шаблон "{name}" не найден.', nd[1])
    return "ok"


    

