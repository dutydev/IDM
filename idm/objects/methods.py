from enum import Enum


class Methods(Enum):

    PING = "ping"
    ADD_USER = "addUser"
    BAN_EXPIRED = "banExpired"
    SUBSCRIBE_SIGNALS = "subscribeSignals"
    DELETE_MESSAGES = "deleteMessages"
    DELETE_MESSAGES_FROM_USER = "deleteMessagesFromUser"
    DELETE_MESSAGES_BY_TYPE = "messages.deleteByType"
    GROUPBOTS_INVITED = "groupbots.invited"
    MEET_CHAT_DUTY = "meetChatDuty"
    MESSAGES_RECOGNISE_AUDIO_MESSAGE = "messages.recogniseAudioMessage"
    IGNORE_MESSAGES = "ignoreMessages"
    PRINT_BOOKMARK = "printBookmark"
    FORBIDDEN_LINKS = "forbiddenLinks"
    SEND_SIGNAL = "sendSignal"
    SEND_MY_SIGNAL = "sendMySignal"
    HERE_API = "hireApi"
    BAN_GET_REASON = "banGetReason"
    TO_GROUP = "toGroup"
    BIND_CHAT = "bindChat"
