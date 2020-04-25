"""

Tools for vk-bot

"""

from module import Blueprint

bp = Blueprint()
__all__ = (
    "get_chat", "send_msg",
    "bp"
)


async def send_msg(
    peer_id: int,
    message: str,
    attachment: str = None,
    disable_mentions: bool = True
):
    await bp.api.messages.send(**locals(), random_id=0)


async def get_chat(date: int, text: str = "!связать") -> int:
    data = (await bp.api.request("messages.search", {
        "q": text, "count": 5
    }))["items"]
    for i in data:
        if i["date"] == date:
            return i["peer_id"]


