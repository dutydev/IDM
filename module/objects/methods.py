from enum import Enum


class Method(str, Enum):
    PING = "ping"
    IGNORE_MESSAGES = "ignoreMessages"
    BAN_EXPIRED = "banExpired"
    ADD_USER = "addUser"
    SUBSCRIBE_SIGNALS = "subscribeSignals"
    DELETE_MESSAGES = "deleteMessages"
    DELETE_MESSAGES_FROM_USER = "deleteMessagesFromUser"
    PRINT_BOOKMARK = "printBookmark"
    FORBIDDEN_LINKS = "forbiddenLinks"
    SEND_SIGNAL = "sendSignal"
    SEND_MY_SIGNAL = "sendMySignal"
    HIRE_API = "hireApi"
    BAN_GET_REASON = "banGetReason"
    TO_GROUP = "toGroup"
    BIND_CHAT = "bindChat"
