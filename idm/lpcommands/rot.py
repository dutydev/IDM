from .utils import MSI
from ..objects import DB
import time, random


def rot(db, time, vk):
    settings = db.settings
    #адвд
    if settings['friends_add']:
        vk('execute', code = """
        var i = 0;
        var items = API.friends.getRequests({"need_viewed": true}).items;
        items = API.users.get({"user_ids": items});
        while (i < 23 && i <= items.length) {
            if (items[i].deactivated == null){
                API.friends.add({"user_id": items[i].id});
                };
            i = i + 1;
        };""")

    #автоотписка
    if settings['del_requests']:
        vk('execute', code = """
        var i = 0;
        var items = API.friends.getRequests({"out": true}).items;
        while (i < 24 && i <= items.length) {
            if (items[i].deactivated == null){
                API.friends.delete({"user_id": items[i]});
                };
            i = i + 1;
        };""")
    #автоонлайн
    if settings['online']: vk('account.setOnline')

    #автоферма
    farm = settings['farm']
    if farm['on'] and time - farm['last_time'] > 14500:
        vk('wall.createComment', owner_id = -174105461,
        post_id = 35135, message = 'Ферма')
        if farm['soft']:
            farm['last_time'] = time + random.randint(0, 14400)
        else: farm['last_time'] = time

    db.save()
    return time