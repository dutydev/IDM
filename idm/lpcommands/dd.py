#   да, vk.com/broken_heart_gesha, "дд"
#   аче)
from .utils import msg_op, MSI, timenow, exe
from ..objects import DB
import time, re

def msg_del(nd, pr = '.с ', count = 0, msg = 'ы', tn = timenow(), edit = False, vk = ''):
    count = re.search(r'\d+', nd[5])
    excepts = vk.raise_excepts
    if not count: count = 2
    else: count = int(count[0]) + 1
    if 'все' in nd[5]: count = 1000
    if edit:
        vk.raise_excepts = False
        i = 1
        for cmsg in vk('messages.getHistory', peer_id = nd[3], count = 200)['items']:
            if cmsg['out'] == 1:
                resp = msg_op(2, nd[3], msg, msg_id = cmsg['id'])
                if type(resp) != int: break
                i += 1
                if i > count: break
                time.sleep(0.3)
    else: msg_op(2, nd[3], msg, nd[1])

    code = """
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
        if ((items[i].date - tn) > 86400) {count = 0;};
        i = i + 1;
    };
    API.messages.delete({"message_ids": msg_ids,"delete_for_all":"1"});
    return count;
    """ % (tn, count, nd[3])
    for _ in range(5):
        count = exe(code)
        if type(count) == int:
            if count <= 0: break
        else:
            MSI(f'Что-то пошло не так при удалении:\n{count}')
        time.sleep(0.4)
    vk.raise_excepts = excepts
    return "ok"

def msg_edit(nd):
    exe("""
    var i = 0;
    var l = 0;
    var atts = [];
    var cmd_msg = {};
    var msgs = API.messages.getHistory({"peer_id":"%s"}).items;
    var msg_id = 0;

    while (i < 200){
        if (msgs[i].out == 1) {
            if (l == 0) {
                cmd_msg = {"text": msgs[i].text, "id": msgs[i].id,
                "attachments": msgs[i].attachments};
                if (msgs[i].reply_message) {
                    msg_id = msgs[i].reply_message.id;
                };
            };
            if (l == 1 && msg_id == 0) {
                msg_id = msgs[i].id;
            };
            if (l == 2) { i = 200; };
            l = l + 1;
        };
        i = i + 1;
    };
    if (cmd_msg.attachments) {
        i = 0;
        while ( i < cmd_msg.attachments.length) {
            var type = cmd_msg.attachments[i].type;
            if (type != "link") {
            atts.push(type + cmd_msg.attachments[i][type].owner_id +
            "_" + cmd_msg.attachments[i][type].id);
            };
            i = i + 1;
        };
    };
    API.messages.edit({
        "peer_id": "%s","message_id": msg_id,
        "message": cmd_msg.text.substr(4, 10000),
        "attachment": atts
        });
    API.messages.delete({"message_ids": cmd_msg.id, "delete_for_all":"1"});
    return 1;
    """ % (nd[3], nd[3]))