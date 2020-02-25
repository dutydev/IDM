from enum import Enum

class Methods(Enum):
    PING = "ping"
    ADD_USER = "addUser"
    BAN_EXPIRED = "banExpired"
    SUBSCRIBE_SIGNALS = "subscribeSignals"
    DELETE_MESSAGES = "deleteMessages"
    DELETE_MESSAGES_FROM_USER = "deleteMessagesFromUser"
    IGNORE_MESSAGES = "ignoreMessages"
    PRINT_BOOKMARK = "printBookmark"
    FORBIDDEN_LINKS = "forbiddenLinks"
    SEND_SIGNAL = "sendSignal"
    SEND_MY_SIGNAL = "sendMySignal"
    HERE_API = "hireApi"
    BAN_GET_REASON = "banGetReason"
    TO_GROUP = "toGroup"
    BIND_CHAT = "bindChat"