from dutymanager.units.vk_script import msg_edit
from dutymanager.db.methods import AsyncDatabase
from dutymanager.units.utils import *
from module import Blueprint, Method
from module import types

import typing

bot = Blueprint()
db = AsyncDatabase.get_current()
patterns = [
    "шабы", "шабы <page:int>",
    "мои шабы", "мои шабы <page:int>",
]


def from_context(tag: str) -> typing.Optional[str]:
    for k, v in db.templates.items():
        if tag in k:
            return k


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=["+шаб <tag>\n<text>", "+шаб <tag>"]
)
async def add_template(event: types.SendMySignal, tag: str, text: str = None):
    peer_id = db.chats(event.object.chat)
    data = (await get_by_local(
        peer_id, event.object.conversation_message_id
    ))
    attachments = await get_attachments(data)
    if tag.lower() in db.templates:
        return await edit_msg(
            peer_id=peer_id, message_id=data["id"],
            message=await edit_template(tag, text, attachments)
        )

    if not any([attachments, text]):
        return await edit_msg(
            peer_id, data["id"], "❗ Шаблон не может быть пустым."
        )
    await db.templates.create(tag, text, attachments)
    db.create_pages(db.settings())
    await edit_msg(
        peer_id, data["id"], f"✅ Шаблон «{tag.lower()}» успешно добавлен."
    )


async def edit_template(*args) -> str:
    tag, text, attachments = args
    if not any([attachments, text]):
        return "❗ Шаблон не может быть пустым."

    await db.templates.change(
        tag, text=text, attachments=attachments
    )
    return f"✅ Шаблон «{tag.lower()}» успешно отредактирован."


@bot.event.message_signal(Method.SEND_MY_SIGNAL, text="-шаб <tag>")
async def remove_template(event: types.SendMySignal, tag: str):
    peer_id = db.chats(event.object.chat)
    local_id = event.message.conversation_message_id
    if tag.lower() not in db.templates:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message=f"❗ Шаблон «{tag.lower()}» не найден."
        )
    await db.templates.remove(tag)
    db.create_pages(db.settings())
    await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message=f"❗ Шаблон «{tag.lower()}» удален."
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text=patterns
)
async def get_templates(event: types.SendMySignal, page: int = 1):
    peer_id = db.chats(event.object.chat)
    local_id = event.message.conversation_message_id
    if page not in db.pages:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="⚠ Ошибка, страница не найдена.",
        )
    array = [f"{n + 1}. {k}" for n, k in enumerate(db.pages[page])]
    await msg_edit(
        peer_id=peer_id, local_id=local_id,
        message="🗓 Мои шаблоны (страница {} из {}):\n{}".format(
            page, len(db.pages), "\n".join(array)
        )
    )


@bot.event.message_signal(
    Method.SEND_MY_SIGNAL,
    text="шаб <tag>",
    lower=True
)
async def get_template(event: types.SendMySignal, tag: str):
    template = from_context(tag)
    peer_id = db.chats(event.object.chat)
    local_id = event.object.conversation_message_id
    if not template:
        return await msg_edit(
            peer_id=peer_id, local_id=local_id,
            message="❗ Нет у меня шаблона с таким названием."
        )

    await msg_edit(
        peer_id=peer_id, local_id=local_id,
        **db.templates(template)
    )