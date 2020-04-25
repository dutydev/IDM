from module import Blueprint, Method
from module import types
from dutymanager.units.utils import *
from dutymanager.db.methods import AsyncDatabase

import typing

bot = Blueprint()
db = AsyncDatabase.get_current()


def from_context(tag: str) -> typing.Optional[str]:
    for k, v in db.templates.items():
        if tag in k:
            return k


@bot.on.message_event(
    Method.SEND_MY_SIGNAL,
    text=["+шаб <tag>\n<text>", "+шаб <tag>"]
)
async def add_template(event: types.SendMySignal, tag: str, text: str = None):
    peer_id = db.chats[event.object.chat]
    data = (await get_by_local(
        peer_id, event.object.conversation_message_id
    ))
    attachments = await get_attachments(data)
    if tag.lower() in db.templates:
        return await edit_msg(
            peer_id=peer_id,
            message_id=data["id"],
            message=await edit_template(tag, text, attachments)
        )

    if not any([attachments, text]):
        return await edit_msg(
            peer_id, data["id"], "❗ Шаблон не может быть пустым."
        )
    await db.add_template(tag, text, attachments)
    await edit_msg(
        peer_id, data["id"], f"✅ Шаблон «{tag.lower()}» успешно добавлен."
    )


async def edit_template(tag: str, *args) -> str:
    text, attachments, message_id = args
    if not any([attachments, text]):
        return "❗ Шаблон не может быть пустым."

    await db.edit_template(tag.lower(), text, attachments)
    return f"✅ Шаблон «{tag.lower()}» успешно отредактирован."


@bot.on.message_event(Method.SEND_MY_SIGNAL, text="-шаб <tag>")
async def remove_template(event: types.SendMySignal, tag: str):
    peer_id = db.chats[event.object.chat]
    message_id = (await get_by_local(
        peer_id, event.object.conversation_message_id
    ))["id"]
    if tag.lower() not in db.templates:
        return await edit_msg(
            peer_id,
            message_id,
            f"❗ Шаблон «{tag.lower()}» не найден."
        )
    await db.remove_template(tag.lower())
    await edit_msg(
        peer_id, message_id, f"❗ Шаблон «{tag.lower()}» удален."
    )


@bot.on.message_event(
    Method.SEND_MY_SIGNAL,
    text=["мои шабы", "шаблоны", "шабы"]
)
async def get_templates(event: types.SendMySignal):
    peer_id = db.chats[event.object.chat]
    message_id = (await get_by_local(
        peer_id, event.object.conversation_message_id
    ))["id"]
    templates = [f"{n + 1}. {k}" for n, k in enumerate(db.templates)]
    await edit_msg(
        peer_id,
        message_id,
        "🗓 Мои шаблоны:\n{}".format("\n".join(templates))
    )


@bot.on.message_event(
    Method.SEND_MY_SIGNAL,
    text="шаб <tag>",
    lower=True
)
async def get_template(event: types.SendMySignal, tag: str):
    template = from_context(tag)
    peer_id = db.chats[event.object.chat]
    local_id = event.object.conversation_message_id
    message_id = (await get_by_local(
        peer_id, local_id
    ))["id"]
    if not template:
        return await edit_msg(peer_id, message_id, "❗ Нет у меня шаблона с таким названием.")

    await edit_msg(peer_id, message_id, **db.templates[template])