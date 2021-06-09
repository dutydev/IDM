import re
from typing import Tuple, Union

from idm.utils import att_parse
from idm.objects import MySignalEvent, dp


def delete_template(name: str, templates: list) -> Tuple[list, bool]:
    for template in templates:
        if template['name'].lower() == name:
            templates.remove(template)
            return templates, True
    return templates, False


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
    event.db.save()

    event.msg_op(2, f'✅ Шаблон "{name}" ' +
                 ("перезаписан" if exist else "сохранен"), delete=2)
    return "ok"


@dp.longpoll_event_register('шабы')
@dp.my_signal_event_register('шабы')
def template_list(event: MySignalEvent) -> str:
    category = ' '.join(event.args).lower()
    templates = event.db.templates
    if category == 'все':
        message = '📃 Список всех шаблонов:'
        for i, t in enumerate(templates, 1):
            message += f"\n{i}. {t['name']} | {t['cat']}"
    elif not category:
        cats = {}
        for t in templates:
            cats[t['cat']] = cats.get(t['cat'], 0) + 1
        message = "📚 Категории шаблонов:"
        for cat in cats:
            message += f"\n-- {cat} ({cats[cat]})"
    else:
        message = f'📖 Шаблоны категории "{category}":'
        for t in templates:
            if t['cat'] == category:
                message += f"\n-- {t['name']}"
    if '\n' not in message:
        if templates == []:
            message = '👀 Нет ни одного шаблона... Для создания используй команду "+шаб"'  # noqa
        else:
            message = '⚠️ Шаблоны по указанному запросу не найдены'
    event.msg_op(2, message)
    return "ok"


def get_name(event: MySignalEvent) -> Union[str]:
    return event, ' '.join(event.args).lower()


@dp.longpoll_event_register('-шаб')
@dp.my_signal_event_register('-шаб')
@dp.wrap_handler(get_name)
def template_delete(event: MySignalEvent, name: str) -> str:
    event.db.templates, exist = delete_template(name, event.db.templates)
    if exist:
        msg = f'✅ Шаблон "{name}" удален'
        event.db.save()
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
