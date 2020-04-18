from ...objects import dp, MySignalEvent
from ...utils import edit_message
import time

@dp.my_signal_event_handle('ф', 'f')
def fpic(event: MySignalEvent) -> str:
    picl = ['🌕🌗🌑🌑🌑🌑🌑🌓🌕','🌕🌗🌑🌑🌑🌑🌑🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕',
    '🌕🌗🌑🌑🌑🌑🌓🌕🌕','🌕🌗🌑🌑🌑🌑🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕']
    pic0 = picl[0]
    pic1 = picl[1]
    pic2 = picl[2]
    pic3 = picl[3]
    pic4 = picl[4]
    pic5 = picl[5]
    pic6 = picl[6]
    pic7 = picl[7]
    pic8 = picl[8]

    for i in 0, 1, 2, 3, 4, 5, 6, 7, 8, 9:
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
        message=f'{pic0}\n{pic1}\n{pic2}\n{pic3}\n{pic4}\n{pic5}\n{pic6}\n{pic7}\n{pic8}')
        pic0 = pic0[-1:] + pic0[:-1]
        pic1 = pic1[-1:] + pic1[:-1]
        pic2 = pic2[-1:] + pic2[:-1]
        pic3 = pic3[-1:] + pic3[:-1]
        pic4 = pic4[-1:] + pic4[:-1]
        pic5 = pic5[-1:] + pic5[:-1]
        pic6 = pic6[-1:] + pic6[:-1]
        pic7 = pic7[-1:] + pic7[:-1]
        pic8 = pic8[-1:] + pic8[:-1]
        time.sleep(0.8)
    return "ok"