from typing import Union

from vkapi import VkApiResponseException
from ..objects import dp, Event, utils

OK = {'response': 'ok'}


@dp.event_handle(dp.Methods.GROUPBOTS_INVITED)
def groupbots_invited(event: Event) -> Union[str, dict]:
    peer_id = None

    conversations = event.api.method(
        'messages.getConversations'
    )
    for conversation in conversations['items']:
        if conversation['conversation']['peer']['type'] != 'chat':
            continue

        if (
                event.msg['conversation_message_id'] <=
                conversation['last_message']['conversation_message_id'] <
                event.msg['conversation_message_id'] + 300
        ):
            try:

                message = event.api.method(
                    'messages.getByConversationMessageId',
                    peer_id=conversation['conversation']['peer']['id'],
                    conversation_message_ids=event.msg['conversation_message_id']
                )['items'][0]
                if message['from_id'] == event.msg['from_id'] and message['date'] == event.msg['date']:
                    peer_id = message['peer_id']
            except:
                continue
    if not peer_id:
        return {
            'response': 'error',
            'error_code': 10
        }

    group = event.api.method(
        'groups.getById',
        group_ids=event.obj['group_id']
    )[0]
    try:
        event.api.method(
            'messages.setMemberRole',
            role='admin',
            peer_id=peer_id,
            member_id=-event.obj['group_id']
        )
        utils.new_message(
            event.api, peer_id,
            message=f"✅ Группа-бот [club{event.obj['group_id']}|{group['name']}] назначена на роль администратора"
        )
    except VkApiResponseException as ex:
        if ex.error_code == 15:
            utils.new_message(
                event.api, peer_id,
                message=f"⚠ Произошла ошибка при назначении группы-бота [club{event.obj['group_id']}|{group['name']}]"
                        f" на роль администратора. Нет доступа.\n"
                        f"Возможные причины:\n"
                        f"-- Вы не администратор в чате\n"
                        f"-- Это чат сообщества"
            )
            return OK
        utils.new_message(
            event.api, peer_id,
            message=f"⚠ Произошла ошибка при назначении группы-бота [club{event.obj['group_id']}|{group['name']}]"
                    f" на роль администратора.\n"
                    f"Ошибка VkAPI: {ex}"
        )
        return OK
    return {'response': 'ok'}
