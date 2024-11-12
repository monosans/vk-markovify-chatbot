from __future__ import annotations

import charset_normalizer


def bytes_decode(b: bytes, /) -> str:
    return str(charset_normalizer.from_bytes(b)[0])
