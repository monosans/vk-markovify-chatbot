from __future__ import annotations

import ssl
from typing import TYPE_CHECKING

import certifi
import charset_normalizer

from .utils import bytes_decode

if TYPE_CHECKING:
    from aiohttp import ClientResponse

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


class NoCharsetHeaderError(Exception):
    pass


def fallback_charset_resolver(r: ClientResponse, b: bytes) -> str:  # noqa: ARG001
    return charset_normalizer.from_bytes(b)[0].encoding


def get_response_text(*, response: ClientResponse, content: bytes) -> str:
    try:
        return content.decode(response.get_encoding())
    except (NoCharsetHeaderError, UnicodeDecodeError):
        return bytes_decode(content)
