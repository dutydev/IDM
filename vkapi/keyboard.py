import json
import typing

from enum import Enum


class ButtonType(Enum):
    TEXT = "text"
    LOCATION = "location"
    VKPAY = "vkpay"
    OPEN_APP = "open_app"
    OPEN_LINK = "open_link"


class ButtonColor(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    NEGATIVE = "negative"
    POSITIVE = "positive"
    NONE = None


class Keyboard(object):

    def __init__(self, one_time: bool = False, inline: bool = False):
        self.ButtonType: ButtonType
        self.ButtonColor: ButtonColor
        self.one_time: bool = one_time
        self.inline: bool = inline
        self.current_line: int = 0
        self.lines: typing.List[typing.List] = [[]]

        self.keyboard = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": []
        }

    def add_line(self):
        self.lines.append([])
        self.current_line += 1

    def add_button(
        self,
        kind: ButtonType,
        color: ButtonColor,
        label: str = None,
        hash_key: str = None,
        app_id: int = None,
        owner_id: int = None,
        payload: str = None,
        link: str = None
    ):
        button = {}
        action = {}

        if label:
            action["label"] = label

        if kind:
            action["type"] = kind.value

        if hash_key:
            action["hash"] = kind

        if app_id:
            action["app_id"] = app_id

        if owner_id:
            action["owner_id"] = owner_id

        if payload:
            action["payload"] = payload

        if link:
            action["link"] = link

        button["action"] = action
        if color != ButtonColor.NONE:
            button["color"] = color.value

        self.lines[self.current_line].append(button)

    def get(self):
        self.keyboard["buttons"] = self.lines
        return json.dumps(self.keyboard, ensure_ascii=False)
