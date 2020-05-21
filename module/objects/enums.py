from enum import Enum
from typing_extensions import final


class ABCEnum(Enum):
    @classmethod
    @final
    def list(cls):
        return [i.value for i in cls]


class Method(ABCEnum):
    PING = "ping"
    IGNORE_MESSAGES = "ignoreMessages"
    BAN_EXPIRED = "banExpired"
    ADD_USER = "addUser"
    SUBSCRIBE_SIGNALS = "subscribeSignals"
    DELETE_MESSAGES = "deleteMessages"
    DELETE_MESSAGES_FROM_USER = "deleteMessagesFromUser"
    DELETE_MESSAGES_BY_TYPE = "messages.deleteByType"
    PRINT_BOOKMARK = "printBookmark"
    FORBIDDEN_LINKS = "forbiddenLinks"
    SEND_SIGNAL = "sendSignal"
    SEND_MY_SIGNAL = "sendMySignal"
    HIRE_API = "hireApi"
    BAN_GET_REASON = "banGetReason"
    TO_GROUP = "toGroup"
    BIND_CHAT = "bindChat"
    MEET_CHAT_DUTY = "meetChatDuty"


class TokenType(ABCEnum):
    ACCESS_TOKEN = "access_token"
    FRIENDS_TOKEN = "friends_token"
    ONLINE_TOKEN = "online_token"
    ME_TOKEN = "me_token"
