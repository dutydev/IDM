from .. import utils
from ..objects import dp, Event


@dp.event_handle(dp.Methods.SUBSCRIBE_SIGNALS)
def subscribe_signals(event: Event) -> str:
    message = f"""✅ Все отлично. 
        IDM настроен и готов к работе.

        Iris chat ID: {event.chat.iris_id}
        VK peer ID: {event.chat.peer_id}
        Панель управления IDM: https://{event.db.host}/

        Приятного общения :3
        
        PS
        ВК: https://vk.com/llordrall
        GitHub: https://github.com/LordRalInc/IDM
        """.replace("    ", "")

    event.db.chats[event.chat.iris_id]['installed'] = True
    event.db.save()
    utils.new_message(event.api, event.chat.peer_id, message=message)
    return "ok"
