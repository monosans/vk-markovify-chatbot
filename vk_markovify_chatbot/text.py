from __future__ import annotations

import random
import re
from typing import Optional

import markovify

tag_pattern = re.compile(r"\[(\w+?\d+?)\|.+?\]")


def clean_text(text: str) -> str:
    # Удаление пустых строк
    text = text.replace("\n\n", "\n")

    # Удаление пробела в начале строк
    text = text.replace("\n ", "\n")

    # Преобразование [id1|@durov] в @id1
    text = tag_pattern.sub(r"@\1", text)

    return text.lower()


def generate_text(text: str) -> str:
    text_model = markovify.NewlineText(input_text=text, state_size=1, well_formed=False)
    sentence: Optional[str] = text_model.make_sentence(tries=1000)
    if sentence is None:
        return random.choice(text.splitlines())
    return sentence
