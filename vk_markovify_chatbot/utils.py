from __future__ import annotations

from typing import TYPE_CHECKING

import charset_normalizer

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVar

    T = TypeVar("T")
    P = ParamSpec("P")


def bytes_decode(b: bytes, /) -> str:
    return str(charset_normalizer.from_bytes(b)[0])
