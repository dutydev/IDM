from ...objects import dp, MySignalEvent
from ...utils import new_message, edit_message, sticker_message
import random, time

cool = [7259, 4088, 6026, 3136, 13603, 17698, 8887, 10349, 19169, 15729, 9666]

@dp.my_signal_event_handle('стик')
def stickers(event: MySignalEvent) -> str:
    amount = 1
    try:
        if len(event.args) == 2:
            if event.args[0].isdigit() and not event.args[1].isdigit():
                amount = int(event.args[0])
                cat = event.args[1]
            elif event.args[1].isdigit() and not event.args[0].isdigit():
                amount = int(event.args[1])
                cat = event.args[0]
            else:
                new_message(event.api, event.chat.peer_id,
                message=f'ДВА АРГУМЕНТА, ОДИН ИЗ НИХ КОЛИЧЕСТВО, ДРУГОЙ НАЗВАНИЕ, ТУПИЦА!')
                return 'ok'
        else:
            cat = event.args[0]
    except:
        new_message(event.api, event.chat.peer_id, message=f'ХУЙНЮ НЕ ПИШИ БЛЯДЬ')
        return 'ok'

    if cat == 'круто':
        rnd = random.randint(0, (len(cool) - 1))
        while 0 < amount:
            sticker_message(event.api, event.chat.peer_id, cool[rnd])
            del cool[rnd]
            amount -= 1
            rnd = random.randint(0, amount)
            time.sleep(1)
    return "ok"