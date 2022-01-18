from duty.objects import dp, MySignalEvent
from animstarter import start_player
import json
import os


# у меня почему то падает python language server, когда я пихаю смайлики сюда,
# поэтому пришлось их спрятать в json
with open(os.path.join(os.path.dirname(__file__), 'anims.json'),
          encoding='utf-8') as anims:
    data = json.loads(anims.read())
    animations: dict = data['animations']
    rotating_animations: dict = data['rotating_animations']


animation_names = ['зарплата', 'дорога', 'поддержка', 'помощь', 'ф']
animation_names.extend(animations.keys())
animation_names.extend(rotating_animations.keys())


@dp.longpoll_event_register(*animation_names)
@dp.my_signal_event_register(*animation_names)
def animation_play(event: MySignalEvent):
    text = ' '.join(event.msg['text'].split(' ')[1:])
    
    if text in {'ф', 'f', 'луна', 'ъуъ'}:
        if text == 'ф':
            text = text.replace('ф', 'f')
        pics = rotating_animations.get(text)
        start_player(event.chat.peer_id, event.msg['id'], event.db.access_token, pics, 1, False)
        return "ok"

    if 'зарплата' in text:
        text = text.replace('зарплата', 'зп')
    elif 'дорога' in text:
        text = text.replace('дорога', 'дрг')
    elif 'поддержка' in text:
        text = text.replace('поддержка', 'под')
    elif 'помощь' in text:
        text = text.replace('помощь', 'под')

    pic = animations.get(text)
    if pic:
        start_player(event.chat.peer_id, event.msg['id'], event.db.access_token, pic, 1, True)
    return "ok"