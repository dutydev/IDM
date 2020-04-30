from .base import BaseModel
from typing import Any, List


class BaseObject(BaseModel):
    method: str
    user_id: int
    secret: str


class Message(BaseModel):
    conversation_message_id: int
    from_id: int
    date: int
    text: str


class BanExpiredObject(BaseModel):
    user_id: int
    chat: str
    comment: str


class AddUserObject(BaseModel):
    user_id: int
    chat: str


class SubscribeSignalsObject(BaseModel):
    chat: str
    conversation_message_id: int
    text: str
    from_id: int


class DeleteMessagesObject(BaseModel):
    chat: str
    local_ids: List[int]
    is_spam: int


class DeleteMessagesFromUserObject(BaseModel):
    chat: str
    member_ids: List[int]
    user_id: int
    amount: int = 1000
    is_spam: int


class IgnoreMessagesObject(BaseModel):
    chat: str
    local_ids: List[int]


class PrintBookmarkObject(BaseModel):
    chat: str
    conversation_message_id: int
    description: str


class ForbiddenLinksObject(BaseModel):
    chat: str
    local_ids: List[int]


class SendSignalObject(BaseModel):
    chat: str
    from_id: int
    value: str
    conversation_message_id: int


class SendMySignalObject(BaseModel):
    chat: str
    from_id: int
    value: str
    conversation_message_id: int


class HireApiObject(BaseModel):
    chat: str
    price: int


class ToGroupObject(BaseModel):
    chat: str
    group_id: int
    local_id: int


class BanGetReasonObject(BaseModel):
    chat: str
    local_id: int


class BindChatObject(BaseModel):
    chat: str


class Ping(BaseObject):
    object: Any


class BindChat(BaseObject):
    message: Message
    object: BindChatObject


class BanExpired(BaseObject):
    object: BanExpiredObject


class AddUser(BaseObject):
    object: AddUserObject


class SubscribeSignals(BaseObject):
    message: Message
    object: SubscribeSignalsObject


class DeleteMessages(BaseObject):
    object: DeleteMessagesObject


class DeleteMessagesFromUser(BaseObject):
    message: Message
    object: DeleteMessagesFromUserObject


class IgnoreMessages(BaseObject):
    object: IgnoreMessagesObject


class PrintBookmark(BaseObject):
    object: PrintBookmarkObject


class ForbiddenLinks(BaseObject):
    object: ForbiddenLinksObject


class SendSignal(BaseObject):
    message: Message
    object: SendSignalObject


class SendMySignal(BaseObject):
    message: Message
    object: SendSignalObject


class HireApi(BaseObject):
    object: HireApiObject


class BanGetReason(BaseObject):
    object: BanGetReasonObject


class ToGroup(BaseObject):
    object: ToGroupObject


BindChat.update_forward_refs()
SendSignal.update_forward_refs()
BanExpired.update_forward_refs()
AddUser.update_forward_refs()
SubscribeSignals.update_forward_refs()
DeleteMessages.update_forward_refs()
DeleteMessagesFromUserObject.update_forward_refs()
PrintBookmark.update_forward_refs()
ForbiddenLinks.update_forward_refs()
SendSignal.update_forward_refs()
SendMySignal.update_forward_refs()
HireApi.update_forward_refs()
BanGetReason.update_forward_refs()
ToGroup.update_forward_refs()