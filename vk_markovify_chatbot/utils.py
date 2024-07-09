from __future__ import annotations

import asyncio
import functools
from typing import TYPE_CHECKING

import charset_normalizer

if TYPE_CHECKING:
    from typing import Callable

    from typing_extensions import ParamSpec, TypeVar

    T = TypeVar("T")
    P = ParamSpec("P")


def bytes_decode(b: bytes, /) -> str:
    return str(charset_normalizer.from_bytes(b)[0])


def asyncify(f: Callable[P, T], /) -> Callable[P, asyncio.Future[T]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> asyncio.Future[T]:
        return asyncio.get_running_loop().run_in_executor(
            None, functools.partial(f, *args, **kwargs)
        )

    return functools.update_wrapper(wrapper, f)
