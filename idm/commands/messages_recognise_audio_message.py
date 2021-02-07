import time
from typing import Union, Optional

from ..objects import dp, Event


def get_transcript(message: dict) -> Optional[str]:
    for attachment in message['attachments']:
        if attachment['type'] == 'audio_message':
            if attachment['audio_message']['transcript_state'] == 'done':
                return attachment['audio_message']['transcript']


@dp.event_handle(dp.Methods.MESSAGES_RECOGNISE_AUDIO_MESSAGE)
def messages_recognise_audio_message(event: Event) -> Union[str, dict]:
    if not event.chat:
        return {
            "response": "error",
            "error_code": 4
        }

    message = event.api.method(
        "messages.getByConversationMessageId",
        peer_id=event.chat.peer_id,
        conversation_message_ids=event.obj['local_id']
    )['items'][0]
    transcript = get_transcript(message)
    if transcript is None:
        time.sleep(1)
        message = event.api.method(
            "messages.getByConversationMessageId",
            peer_id=event.chat.peer_id,
            conversation_message_ids=event.obj['local_id']
        )['items'][0]
        transcript = get_transcript(message)
        if transcript is None:
            time.sleep(4)
            message = event.api.method(
                "messages.getByConversationMessageId",
                peer_id=event.chat.peer_id,
                conversation_message_ids=event.obj['local_id']
            )['items'][0]
            transcript = get_transcript(message)
            user = event.api.method("users.get", user_ids=message['from_id'])[0]
            name = f"[id{user.id}|{user.first_name} {user.last_name}]"
            if transcript:
                text = f"💬 {name}: {transcript}"
            else:
                text = f"💬 {name}: Сказал что-то не внятное"
            event.api.method(
                "messages.send",
                peer_id=event.chat.peer_id,
                random_id=0,
                message=text
            )
            return {"response": "ok"}
    return {
        'transcript': transcript,
        "response": "ok"
    }
