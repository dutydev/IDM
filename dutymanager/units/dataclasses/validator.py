from vbml import Patcher, PatchedValidators
from dutymanager.units.tools import parse_interval
from typing import Optional


class Validator(PatchedValidators):
    def unix(self, value: str) -> Optional[int]:
        interval = parse_interval(value)
        if interval:
            return int(interval)


patcher = Patcher(validators=Validator, pattern="^{}$")