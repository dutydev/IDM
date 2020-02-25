import enum
import json

class ButtonType(enum.Enum):
    TEXT = "text"
    LOCATION ="location"
    VKPAY = "vkpay"
    OPEN_APP = "open_app"
    OPEN_LINK = "open_link"

class ButtonColor(enum.Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary" 
    NEGATIVE = "negative" 
    POSITIVE = "positive"
    NONE = None

class Keyboard(object):
    ButtonType: ButtonType
    ButtonColor: ButtonColor

    one_time: bool
    inline: bool
    keyboard: dict
    lines: list

    cureit_line: int

    def __init__(self, one_time: bool, inline: bool):
        self.ButtonType = ButtonType
        self.ButtonColor = ButtonColor


        self.one_time = one_time
        self.inline = inline
        self.cureit_line = 0
        self.lines = [[]]

        self.keyboard = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": []
        }

    def add_line(self):
        self.lines.append([])
        self.cureit_line += 1

    def add_button(self, type: ButtonType, color: ButtonColor, label: str = None,
                    hash: str = None, app_id: int = None,
                    owber_id: int = None, payload: str = None, link: str = None):
        button = {} # action color
        action = {} 

        if label != None: action["label"] = label
        if type != None: action["type"] = type.value
        if hash != None: action["hash"] = hash
        if app_id != None: action["app_id"] = app_id
        if owber_id != None: action["owber_id"] = owber_id
        if payload != None: action["payload"] = payload
        if link != None: action["link"] = link

        button["action"] = action
        if color != ButtonColor.NONE:
            button["color"] = color.value 

        self.lines[self.cureit_line].append(button)

    def get(self):
        self.keyboard["buttons"] = self.lines
        return json.dumps(self.keyboard, ensure_ascii=False)
        

