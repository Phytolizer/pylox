from typing import Optional


class LoxObject:
    value: Optional[object]

    def __init__(self, obj: Optional[object]):
        self.value = obj

    def __str__(self) -> str:
        if self.value is None:
            return "nil"
        if isinstance(self.value, float):
            return str(self.value).replace(".0", "")
        return str(self.value)
