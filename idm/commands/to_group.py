# TODO: переписать, добавить параметры
import typing
from idm.api_utils import get_msg
from ..objects import dp, Event
from microvk import VkApiResponseException
import re
import requests

@dp.event_register('toGroup')
def to_group(event: Event) -> str:
    def parse_attachments(event: Event) -> typing.Tuple[str, typing.List[str]]:
        def get_payload(text: str) -> str:
            regexp = r"(^[\S]+)|([\S]+)|(\n[\s\S \n]+)"
            _args = re.findall(regexp, text)
            payload = ""
            for arg in _args:
                if arg[2] != '':
                    payload = arg[2][1:]
            return payload

        def upload_photo(url: str) -> str:
            server = event.api("photos.getWallUploadServer", group_id=event.obj['group_id'])
            photo = requests.get(url).content
            with open('tmp.jpg', 'wb') as f:
                f.write(photo)

            data = requests.post(server['upload_url'], files={'photo':open('tmp.jpg',"rb")}).json()
            attach = event.api("photos.saveWallPhoto", group_id=event.obj['group_id'], **data)[0]

            return f"photo{attach['owner_id']}_{attach['id']}_{attach['access_key']}"

        payload = get_payload(event.msg['text'])

        attachments = []
        if event.reply_message != None:
            if payload == "":
                payload = event.reply_message['text']
            message = get_msg(event.api, event.chat.peer_id, event.reply_message['conversation_message_id'])
            for attachment in message.get('attachments', []):
                
                a_type = attachment['type']

                if a_type in ['link']:continue

                if a_type == 'photo':
                    attachments.append(upload_photo(
                        attachment['photo']['sizes'][len(attachment['photo']['sizes']) - 1]['url']
                    ))
                else:
                    attachments.append(
                            f"{a_type}{attachment[a_type]['owner_id']}_{attachment[a_type]['id']}_{attachment[a_type]['access_key']}"
                        )

        attachments.extend(event.attachments)   
        return payload, attachments

    text, attachments = parse_attachments(event)

    try:
        data = event.api('wall.post', owner_id=(-1) * event.obj['group_id'], from_group=1, message=text, 
            attachments=",".join(attachments))

        event.send(event.responses['to_group_success'],
            attachment=f"wall-{event.obj['group_id']}_{data['post_id']}")
    except VkApiResponseException as e:
        if e.error_code == 214:
            event.send(event.responses['to_group_err_forbidden'])
        elif e.error_code == 220:
            event.send(event.responses['to_group_err_recs'])
        elif e.error_code == 222:
            event.send(event.responses['to_group_err_link'])
        else:
            event.send(event.responses['to_group_err_vk'] + str({e.error_msg}))
    except:
        event.send(event.responses['to_group_err_unknown'])

    return "ok"