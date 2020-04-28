from ...objects import dp, MySignalEvent
from ...utils import new_message, edit_message
#################    не смотрите сюда мне стыдно  ####################
@dp.my_signal_event_handle('+викосиф', '+викиосиф', '+wikosif', '+wikiosif', '+wikosiph', '+wikiosiph')
def WIadd(event: MySignalEvent) -> str:

    wtfmsg = f"""ДА ХУЛИ ТЫ ОТ МЕНЯ ХОЧЕШЬ, ЕБАЛА?!
    КУДА Я ТЕБЕ, БЛЯДЬ, ЕГО ЗАПИШУ, ЕСЛИ ТЫ МЕНЯ К БД НЕ ПРИКРУТИЛ?!?!
    ПОШЕЛ НАХУЙ ПИЗДАНУТЫЙ
        """.replace("    ", "")
    if ((event.payload == '' or event.payload == None) and len(event.attachments) == 0) or len(event.args) == 0:
            new_message(event.api, event.chat.peer_id, message=wtfmsg)
            return "ok"

    name = " ".join(event.args)
    data = event.payload

    for temp in event.db.templates:
        if temp['name'] == name:
            event.db.templates.remove(temp)
            event.db.save()
            
    event.db.templates.append(
        {
            "name":name,
            "payload":data,
            "attachments":event.attachments
        }
    )
    event.db.save()
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"✅ Шаблон \"{name}\" сохранен.")
    return "ok"


@dp.my_signal_event_handle('-шаб')
def WIremove(event: MySignalEvent) -> str:
        
    if len(event.args) == 0:
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Нет данных")

    name = " ".join(event.args)

    for temp in event.db.templates:
        if temp['name'] == name:
            event.db.templates.remove(temp)
            event.db.save()
            edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"✅Шаблон \"{name}\" удален.")
            return "ok"
    
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"❗ Шаблон \"{name}\" не найден.")
    return "ok"


@dp.my_signal_event_handle('викосиф', 'викиосиф', 'wikosif', 'wikiosif', 'wikosiph', 'wikiosiph')
def WIlist(event: MySignalEvent) -> str:

    _message = "WikIosif"
    itr = 0
    for temp in event.db.templates:
        itr += 1
        _message += f"\n{itr}. {temp['name']}"

    new_message(event.api, event.chat.peer_id, message=_message)
    return "ok"

@dp.my_signal_event_handle('викосиф', 'викиосиф', 'wikosif', 'wikiosif', 'wikosiph', 'wikiosiph')
def run_template(event: MySignalEvent) -> str:
    
    if len(event.args) == 0:
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message="❗ Нет данных")
    if event.args[0] == 'помощь' or event.args[0] == 'help':
        msg = f"""Ты ебу дал, мальчик? 🤔
        Понимаешь, что ты нихуя в этом скрипте не написал, кроме этого сообщения?
        Хули ты от меня хочешь? Пиздуй бороздуй дописывать, сука
        """.replace("    ", "")
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=msg)
    name = " ".join(event.args)

    for temp in event.db.templates:
        if temp['name'] == name:
            edit_message(event.api, event.chat.peer_id, event.msg['id'], message=temp['payload'], attachment=",".join(temp['attachments']))
            return "ok"
    
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f"❗ Шаблон \"{name}\" не найден.")
    return "ok"
