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
    "get_name", "get_requests",
    'get_users'
)


def get_attachments(obj: dict) -> Optional[str]:
    attachments = []
    if not obj["attachments"]:
        return
    for x in obj["attachments"]:
        kind = x["type"]
        if kind == "link":
            continue
        if "access_key" in x[kind]:
            string = "{}{}_{}_{}"
        else:
            string = "{}{}_{}"
        attachments.append(string.format(
            kind, x[kind]["owner_id"],
            x[kind]["id"], x[kind].get("access_key")
        ))
    return ",".join(attachments)


def get_users(obj: dict) -> Optional[list]:
    if obj.get("reply_message"):
        return [obj["reply_message"]["from_id"]]

    if obj["fwd_messages"]:
        return list(set([
            i["from_id"] for i in obj["fwd_messages"]
            if i["from_id"] > 0
        ]))


async def get_requests(count: int = 1000, out: bool = False) -> list:
    return (await bp.api.request("friends.getRequests", {
        "count": count,
        "out": out,
        "extended": 0 if out else 1
    }))["items"]


async def get_name(user_ids: Union[int, list]) -> Union[dict, str]:
    users = await bp.api.users.get(user_ids=user_ids)
    if len(user_ids) == 1:
        return f"{users[0].first_name} {users[0].last_name}"

    return {
        i.id: f"{i.first_name} {i.last_name}"
        for i in users
    }


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