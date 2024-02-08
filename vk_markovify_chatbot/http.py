from __future__ import annotations

import ssl

import certifi
import charset_normalizer
from aiohttp import ClientResponse

from .utils import bytes_decode

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
