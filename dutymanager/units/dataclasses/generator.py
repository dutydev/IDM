from vkbottle.api.api.api import AbstractTokenGenerator
from random import choice
from typing import List, Union


class Generator(AbstractTokenGenerator):
    def __init__(
        self,
        tokens: Union[str, List[str]],
        me_token: str = None,
        online_token: str = None,
        friends_token: str = None,
    ):
        self.me_token = me_token
        self.tokens = tokens if isinstance(tokens, list) else [tokens]
        self.online_token = online_token
        self.friends_token = friends_token

    async def get_token(self, method: str, params: dict) -> str:
        if method in ("messages.setActivity", "messages.send"):
            return self.me_token or choice(self.tokens)

        if method == "account.setOnline":
            return self.online_token

        if method.startswith("friends"):
            return self.friends_token
        return choice(self.tokens)