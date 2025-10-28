import inspect
import re
from dataclasses import dataclass
from abc import ABC


class Validatable(ABC):
    def validate(self) -> list[TypeError]:
        """Validates attributes using line-ending comments left after them. Hell yeah!"""
        src, _ = inspect.getsourcelines(self.__class__)
        regex = re.compile("^\\s+(\\w+):\\s*(\\w+)\\s*#\\s*(.*it.*)$")
        errs: list[TypeError] = []
        for line in src:
            match = regex.match(line)
            if match is None: continue
            attr_name, attr_type, attr_cond = match.group(1, 2, 3)
            cond_callable = eval(f"lambda it: {attr_cond}")
            attr_val = getattr(self, attr_name)
            if not isinstance(attr_val, eval(attr_type)):
                errs.append(TypeError(f"{attr_name} = {attr_val}: Wanted type {attr_type}, got type {type(attr_val)}"))
                continue
            if not cond_callable(attr_val):
                errs.append(TypeError(f"{attr_name} = {attr_val}: Failed validation {attr_cond}"))
        return errs

@dataclass
class TestData(Validatable):
    epic_sauce: int # it < 420 and it % 5 == 0
    power_level: int # it > 9000
