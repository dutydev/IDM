"""

File to work with VK Script compilation

"""
from module import Blueprint
from module.utils import logger

bot = Blueprint(name="VK Script")
__all__ = (
    'execute', 'get_chat',
    'msg_edit', 'msg_send',
    'delete_messages',
    'friends_add', 'friends_delete'
)


async def execute(code: str):
    return await bot.api.request(
        "execute", {"code": code}
    )


async def friends_delete(requests: list):
    code = """var requests = [%s];
    var a = 0;
    while (a < request.length) {
        API.friends.delete({"user_id": requests[a]});
        a = a + 1;
    }
    return 1;"""
    for i in range(0, len(requests), 25):
        await execute(code % requests[i: i + 25])


async def friends_add(requests: list):
    code = """var requests = [%s];
    var a = 0;
    while (a < requests.length) {
        API.friends.add({"user_id": requests[a], "follow": 0});
        a = a + 1;
    }
    return 1;"""
    for i in range(0, len(requests), 25):
        await execute(code % requests[i: i + 25])


async def delete_messages(peer_id: int, local_ids: list, spam: int):
    local_ids = ",".join(list(map(str, local_ids)))
    code = """return API.messages.delete({
    "delete_for_all": 1,
    "spam": %s,
    "message_ids": API.messages.getByConversationMessageId({
        "peer_id": %s, "conversation_message_ids": [%s]
    }).items@.id
    });""" % (spam, peer_id, local_ids)
    logger.debug("Formatting result:\n{}", code)
    return await execute(code)


async def get_chat(date: int, q: str = "!связать"):
    code = """var a = 0;
    var chat_id;
    var title;
    var data = API.messages.search({
        "q": "%s", "count": 5
    }).items;
    while (a < data.length) {
        if (data[a].date == %s) {
            chat_id = data[a].peer_id - 2000000000;
            title = API.messages.getChat({"chat_id": chat_id}).title;
            API.messages.edit({
                "peer_id": data[a].peer_id,
                "message": "✅ Беседа " + "«" + title + "»" + " распознана!",
                "message_id": data[a].id
            });
        return [data[a].peer_id, title];
        }
        a = a + 1;
    }""" % (q, date)
    logger.debug("Formatting result:\n{}", code)
    return await execute(code)


async def msg_edit(peer_id: int, message: str, local_id: int):
    """
    Two methods in one request.
    messages.edit + messages.getByConversationMessageId
    """
    text = message.replace("\n", "\\n")
    code = """return API.messages.edit({
    "peer_id": %s,
    "message": "%s",
    "message_id": API.messages.getByConversationMessageId({
        "peer_id": %s, "conversation_message_ids": %s
    }).items@.id
    });""" % (peer_id, text, peer_id, local_id)
    logger.debug("Formatting result:\n{}", code)
    return await execute(code)


async def msg_send(peer_id: int, message: str, local_id: int):
    """
    Two methods in one request
    messages.send + messages.getByConversationMessageId
    """
    text = message.replace("\n", "\\n")
    code = """return API.messages.send({
    "peer_id": %s,
    "message": "%s",
    "random_id": 0,
    "reply_to": API.messages.getByConversationMessageId({
        "peer_id": %s, "conversation_message_ids": %s
    }).items@.id
    });""" % (peer_id, text, peer_id, local_id)
    logger.debug("Formatting result:\n{}", code)
    return await execute(code)