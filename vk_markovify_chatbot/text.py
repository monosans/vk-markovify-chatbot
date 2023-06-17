from __future__ import annotations

import random
import re
from typing import Sequence

import markovify

tag_pattern = re.compile(r"\[(id\d+?)\|@[\d_a-z]+?\]")


def clean_text(text: str) -> str:
    # Удаление пустых строк
    text = text.replace("\n\n", "\n")

    # Удаление пробела в начале строк
    text = text.replace("\n ", "\n")

    # Преобразование [id1|@durov] в @id1
    text = tag_pattern.sub(r"@\1", text)

    return text.lower()


def generate_text(history: Sequence[str]) -> str:
    text_model = markovify.NewlineText(
        input_text="\n".join(history), state_size=1, well_formed=False
    )
    return text_model.make_sentence(tries=1000) or random.choice(history)
