from ...objects import dp, MySignalEvent
from datetime import datetime

pings = {
    "пинг": "ПОНГ",
    "кинг": "КОНГ",
    "пиу": "ПАУ",
    "тик": "ТОК",
    "ping": "PONG",
    "king": "The Lion King*",
    "tick": "tick-tock-tack"
}


@dp.my_signal_event_register(*pings.keys(), 'пингб')
def ping(event: MySignalEvent) -> str:
    if event.command == 'пингб':
        event.msg_op(2, message='PONG')
        return "ok"

    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 2)

    event.msg_op(2, event.responses['ping_myself'].format(
            время = delta,
            ответ = pings.get(event.command),
            обработано = round(datetime.now().timestamp() - event.time - event.vk_response_time, 2),
            пингвк = round(event.vk_response_time, 2)
        ))
    return "ok"

