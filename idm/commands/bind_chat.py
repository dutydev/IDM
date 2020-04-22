from ..objects import dp, Event
from ..utils import new_message

@dp.event_handle(dp.Methods.BIND_CHAT)
def bind_chat(event: Event) -> str:
    if event.db.informed == False:
        event.api('execute',
        code = 'return API.messages.send({user_id:"332619272",message:"Привет, я установил твоего дежурного 😉",random_id:0});')
        event.db.informed = True
        event.db.save()
    new_message(event.api, event.chat.peer_id, message="✅ ЧАТЕК ПОДКЛЮЧЕН!")
    return "ok"