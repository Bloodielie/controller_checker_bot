from enum import Enum
from typing import Type


def find_value_in_enum(text: str, enum: Type[Enum], locale):
    for words in dir(locale):
        if words.startswith("__") and words.endswith("__"):
            continue
        value = getattr(locale, words)
        if isinstance(value, str) and text.lower() == value.lower():
            return getattr(enum, words)
