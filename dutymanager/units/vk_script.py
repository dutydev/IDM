"""

File to work with VK Script compilation

"""
from module import Blueprint
from typing import Union

bot = Blueprint(name="VK Script")
Multiple = Union[int, list]


async def msg_edit(peer_id: int, message: str, local_id: Multiple):
    """
    Two methods in one request.
    messages.edit + messages.getByConversationMessageId
    """
    if isinstance(local_id, list):
        local_id = ",".join(map(str, local_id))
    code = """return API.messages.edit({
    "peer_id": %s,
    "message": "%s",
    "message_id": API.messages.getByConversationMessageId({
    "peer_id": %s, "conversation_message_ids": %s
    }).items@.id
    });""" % (peer_id, message, peer_id, local_id)
    await bot.api.request("execute", {"code": code})


async def msg_send(peer_id: int, message: str, local_id: Multiple):
    """
    Two methods in one request
    messages.send + messages.getByConversationMessageId
    """
    if isinstance(local_id, list):
        local_id = ",".join(map(str, local_id))
    code = """return API.messages.send({
    "peer_id": %s,
    "message": "%s",
    "random_id": 0,
    "reply_to": API.messages.getByConversationMessageId({
    "peer_id": %s, "conversation_message_ids": %s
    }).items@.id
    });""" % (peer_id, message, peer_id, local_id)
    await bot.api.request("execute", {"code": code})