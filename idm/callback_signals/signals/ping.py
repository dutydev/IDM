from idm.objects import dp, SignalEvent
from datetime import datetime


@dp.signal_event_register('пинг', 'пиу', 'кинг', 'тик')
def ping(event: SignalEvent) -> str:
    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 2)

    r_type = ('ПОНГ' if event.command == "пинг" else "ПАУ" if event.command == "пиу"
    else "ТОК" if event.command == "тик" else "КОНГ")

    event.send(event.responses['ping_duty'].format(время = delta, ответ = r_type))
    return "ok"