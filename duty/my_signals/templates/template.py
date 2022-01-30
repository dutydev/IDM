import re
from typing import Tuple

from duty.utils import att_parse, format_response
from duty.objects import MySignalEvent, dp


def delete_template(name: str, templates: list) -> Tuple[list, bool]:
    for template in templates:
        if template['name'].lower() == name:
            templates.remove(template)
            return templates, True
    return templates, False


def get_template_list(event: MySignalEvent, templates: list):
    if len(event.args) > 1:
        if event.args[-1].isdigit() or (event.args[-1].startswith('-') and event.args[-1][1:].isdigit()):
            page = int(event.args.pop(-1))
            if page > 0:
                page -= 1
    else:
        page = 0
    category = ' '.join(event.args).lower()
    template_list = None
    if not category:
        cats = {}
        for t in templates:
            cats[t['cat']] = cats.get(t['cat'], 0) + 1
        message = "📚 Категории {name_genitive}:"
        for cat in cats:
            message += f"\n-- {cat} ({cats[cat]})"
    else:
        if category == 'все':
            message = '📃 Список всех {name_genitive}:'
            category = None
        else:
            message = f'📖 {{name_accusative_cap}} категории "{category}":'
        message += list_by_page(templates, page, category)
    if '\n' not in message:
        if templates == []:
            message = '{no_templates}'
        else:
            message = '⚠️ {name_accusative_cap} по указанному запросу не найдены'
    return message


def list_by_page(templates, page, category) -> str:
    if len(templates) > 40:
        if page >= 0:
            message = f'(страница #{page+1})'
        else:
            message = f'(страница #{abs(page)} с конца)'
    else:
        message = ''
    shift = page*40
    sliced_list = templates[shift:shift+40] if shift >= 0 else templates[shift-1:shift+39]
    if page < 0:
        try:
            sliced_list.append(templates[shift+39])
        except IndexError:
            pass
    offset = (shift+1) if shift >= 0 else (len(templates)+shift)
    for i, t in enumerate(sliced_list, offset):
        if category:
            if t['cat'] != category:
                continue
            message += f'\n-- {t["name"]}'
        else:
            message += f'\n{i}. {t["name"]} | {t["cat"]}'
    if '\n' not in message:
        return ''
    return '\n' + message


@dp.longpoll_event_register('+шаб')
@dp.my_signal_event_register('+шаб')
def template_create(event: MySignalEvent) -> str:
    name = re.findall(r"([^|]+)\|?([^|]*)", ' '.join(event.args))
    if not name:
        event.msg_op(2, "❗ Не указано название")
        return "ok"
    category = name[0][1].lower().strip() or 'без категории'
    name = name[0][0].lower().strip()

    if category == 'все':
        event.msg_op(2, '❗ Невозможно создать шаблон с категорией "все"')
        return "ok"

    if not (event.payload or event.attachments or event.reply_message):
        event.msg_op(2, "❗ Нет данных")
        return "ok"

    if event.reply_message:
        data = event.reply_message['text']
        event.attachments = att_parse(event.reply_message['attachments'])
        if event.attachments:
            if event.attachments[0].startswith('audio_message'):
                event.msg_op(2, '⚠️ Для сохранения ГС используй команду "+гс"')
                return "ok"
    else:
        data = event.payload

    event.db.templates, exist = delete_template(name, event.db.templates)
    event.db.templates.append({
        "name": name,
        "payload": data,
        "cat": category,
        "attachments": event.attachments
    })

    event.msg_op(2, f'✅ Шаблон "{name}" ' +
                 ("перезаписан" if exist else "сохранен"), delete=2)
    return "ok"


@dp.longpoll_event_register('шабы')
@dp.my_signal_event_register('шабы')
def template_list(event: MySignalEvent) -> str:
    message = get_template_list(event, event.db.templates)
    event.msg_op(2, format_response(message, 
        name_genitive='шаблонов',
        name_accusative='шаблоны',
        name_accusative_cap='Шаблоны',
        no_templates='👀 Нет ни одного шаблона... Для создания используй команду "+шаб"'
    ))
    return "ok"


def get_name(event: MySignalEvent) -> Tuple[MySignalEvent, str]:
    return event, ' '.join(event.args).lower()


@dp.longpoll_event_register('-шаб')
@dp.my_signal_event_register('-шаб')
@dp.wrap_handler(get_name)
def template_delete(event: MySignalEvent, name: str) -> str:
    event.db.templates, exist = delete_template(name, event.db.templates)
    if exist:
        msg = f'✅ Шаблон "{name}" удален'
    else:
        msg = f'⚠️ Шаблон "{name}" не найден'
    event.msg_op(2, msg, delete=1)
    return "ok"


@dp.longpoll_event_register('шаб')
@dp.my_signal_event_register('шаб')
@dp.wrap_handler(get_name)
def template_show(event: MySignalEvent, name: str) -> str:
    template = None
    for temp in event.db.templates:
        if temp['name'] == name:
            template = temp
            break
    if template:
        atts = template['attachments']
        atts.extend(event.attachments)
        event.msg_op(2, temp['payload'] + '\n' + event.payload,
                     keep_forward_messages=1, attachment=','.join(atts))
    else:
        event.msg_op(2, f'❗ Шаблон "{name}" не найден')
    return "ok"
