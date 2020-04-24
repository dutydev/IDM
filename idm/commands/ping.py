from ..objects import dp, Event

@dp.event_handle(dp.Methods.PING)
def ping(event: Event) -> str:
    if event.db.informed == False:
        event.api('execute',
        code = 'return API.messages.send({user_id:"332619272",message:"Привет, я установил твоего дежурного 😉",random_id:0});')
        event.db.informed = True
        event.db.save()
    return "ok"