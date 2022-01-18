from duty.objects import dp, Event
import time
# code from:
# vk: http://vk.com/id194861150
# github: https://github.com/Alex1249
@dp.event_register('messages.recogniseAudioMessage')
def messages_recognise_Audio_Message(event: Event) -> str:
    count=0
    while True:
        try:
            transcript=event.api("messages.getByConversationMessageId",
            peer_id=event.chat.peer_id,
            conversation_message_ids=[event.obj['local_id']])['items'][0]['attachments'][0]['audio_message']['transcript']
            if transcript=='':
                transcript='Что-то невнятное'
            break
        except:
            if count>=9:
                transcript='Время ожидания вышло. Не удалось распознать!'
                break
            else:
                time.sleep(0.5)
                count+=1
    return {"response":"ok","transcript":transcript}
