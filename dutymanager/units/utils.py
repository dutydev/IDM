"""

Tools for vk-bot

"""

from module import Blueprint

bp = Blueprint()

__all__ = (
    "get_chat", "send_msg",
    "get_msg_id", "get_msg_ids",
    "get_history",
    "bp"
)


async def get_history(peer_id: int, count: int = 200) -> dict:
    history = (await bp.api.request("messages.getHistory", {
        "peer_id": peer_id, "count": count
    }))["items"]
    return history


async def get_msg_ids(peer_id: int, local_ids: list) -> list:
    data = await bp.api.messages.get_by_conversation_message_id(
        peer_id=peer_id,
        conversation_message_ids=local_ids
    )
    return [str(i['id']) for i in data.items if "action" not in i]


async def get_msg_id(peer_id: int, local_id: int) -> int:
    data = await bp.api.messages.get_by_conversation_message_id(
        peer_id=peer_id,
        conversation_message_ids=local_id
    )
    return data.items[0]['id']


async def send_msg(
    peer_id: int,
    message: str,
    attachment: str = None,
    disable_mentions: bool = True,
    **kwargs
):

    await bp.api.messages.send(
        peer_id=peer_id,
        message=message,
        attachment=attachment,
        disable_mentions=disable_mentions,
        random_id=0,
        **kwargs
    )


async def get_chat(date: int, text: str = "!связать") -> int:
    data = (await bp.api.request("messages.search", {
        "q": text, "count": 5
    }))["items"]
    for i in data:
        if i["date"] == date:
            return i["peer_id"]


