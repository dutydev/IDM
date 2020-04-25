from vbml import Patcher, PatchedValidators
from .tools import parse_interval

import typing


class Validator(PatchedValidators):
    def unix(self, value: str) -> typing.Optional[int]:
        interval = parse_interval(value)
        if interval:
            return int(interval)


patcher = Patcher(validators=Validator)