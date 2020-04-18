from ...objects import dp, MySignalEvent
from ...utils import edit_message, new_message, delete_message

@dp.my_signal_event_handle('зам', 'замени', 'з')
def replace(event: MySignalEvent) -> str:
    text = " ".join(event.args)
    if event.args[0] == 'помощь':
        text = 'здесь будет помощь по команде'
    else:
        text1 = text.replace('клоун', '🤡')
        text = text.replace('клкл', '👍🏻')
        text = text.replace('кркр', '😎')
        text = text.replace('мдаа', '😐')
        text = text.replace('хмхм', '🤔')
    new_message(event.api, event.chat.peer_id, message=text1)
    return "ok"