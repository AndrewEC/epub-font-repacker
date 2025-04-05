from typing import Any


def fully_qualified_name(cls: Any) -> str:
    return cls.__module__ + '.' + cls.__name__
