from .utils import msg_op
from datetime import datetime
from ..objects import DB
from . import dlp
import time


@dlp.register('пинг', 'кинг', 'пиу', 'тик')
def ping(nd):
    delta = round(nd.time - nd[4], 4)

    r_type = ('ПОНГ' if nd[5] == "пинг" else "ПАУ" if nd[5] == "пиу"
    else "ТОК" if nd[5] == "тик" else "КОНГ")

    if nd[5] == ".с тик":
        time.sleep(1)

    msg = f"{r_type} LP\nПолучено за {delta}с.\nОбработано за "

    msg_op(2, nd[3], msg +
    f'{round(datetime.now().timestamp() - nd.time, 4)}с.', nd[1])