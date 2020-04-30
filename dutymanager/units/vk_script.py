"""

File to work with VK Script compilation

"""
from module import Blueprint
from module.utils import logger

bot = Blueprint(name="VK Script")
__all__ = (
    'execute', 'get_chat',
    'msg_edit', 'msg_send'
)


async def execute(code: str):
    return await bot.api.request(
        "execute", {"code": code}
    )


async def get_chat(date: int, q: str = "!связать"):
    code = """var a = 0;
    var data = API.messages.search({
        "q": "%s", "count": 5
    }).items;
    while (a < data.length) {
        if (data[a].date == %s) {
            API.messages.send({
                "peer_id": data[a].peer_id,
                "message": "✅ Беседа распознана",
                "random_id": 0
            });
        return data[a].peer_id;
        }
        a = a + 1;
    }""" % (q, date)
    logger.debug(code)
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
    logger.debug(code)
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
    logger.debug(code)
    return await execute(code)