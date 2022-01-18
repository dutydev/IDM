from duty.objects import dp, MySignalEvent
import re


@dp.longpoll_event_register('-смс', 'дд')
@dp.my_signal_event_register('-смс', 'дд', skip_receiving=True)
def delete_self_message(event: MySignalEvent) -> str:
    count = re.search(r'\d+', event.msg['text'])
    event.api.raise_excepts = False
    if not count:
        count = 2
    else:
        count = int(count[0]) + 1
    if 'все' in event.msg['text']:
        count = 200

    if not event.db.settings['silent_deleting']:
        event.msg_op(2, event.responses['del_self'])

    event.api.exe("""
    var i = 0;
    var msg_ids = {};
    var tn = %s;
    var count = %s;
    var items = API.messages.getHistory({"peer_id":"%s","count":"200", "offset":"0"}).items;
    while (count > 0 && i < items.length) {
        if (items[i].out == 1){
            msg_ids.push(items[i].id);
            count = count - 1;
            };
        if ((tn - items[i].date) > 86400) {count = 0;};
        i = i + 1;
    };
    API.messages.delete({"message_ids": msg_ids,"delete_for_all":"1"});
    return count;
    """ % (event.msg['date'], count, event.chat.peer_id))
    return "ok"
