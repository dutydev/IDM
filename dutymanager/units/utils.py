"""

Tools for vk-bot

"""

from typing import Optional, Union
from module import Blueprint

bp = Blueprint()
__all__ = (
    "send_msg", "edit_msg",
    "get_attachments", "get_msg_ids",
    "get_history", "get_by_local",
    "get_name", "get_requests"
)


async def get_requests(count: int = 1000, out: bool = False) -> list:
    return (await bp.api.request("friends.getRequests", {
        "count": count,
        "out": out,
        "extended": False if out else True
    }))["items"]


async def get_name(user_ids: Union[int, list]) -> dict:
    data = dict()
    if isinstance(user_ids, str):
        user_ids = [user_ids]
    for i in await bp.api.users.get(
        user_ids=",".join(list(map(str, user_ids)))
    ):
        data[i.id] = f"{i.first_name} {i.last_name}"
    return data


async def get_attachments(obj: dict) -> Optional[str]:
    attachments = []
    if not obj["attachments"]:
        return
    for x in obj["attachments"]:
        kind = x["type"]
        if kind != "link":
            attachments.append(
                f"{kind}{x[kind]['owner_id']}_{x[kind]['id']}"
            )
    return ",".join(attachments)


async def get_by_local(peer_id: int, local_id: int) -> dict:
    data = (await bp.api.request("messages.getByConversationMessageId", {
        "peer_id": peer_id,
        "conversation_message_ids": local_id
    }))["items"][0]
    return data


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


async def edit_msg(
    peer_id: int,
    message_id: int,
    message: str,
    attachment: int = None
):
    await bp.api.messages.edit(
        **locals(), keep_forward_messages=True
    )