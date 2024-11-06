# ruff: noqa: E402
from __future__ import annotations

from . import logs

_logs_listener = logs.configure()

import asyncio
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from typing import Callable

    from typing_extensions import Any, TypeVar

    T = TypeVar("T")


def get_async_run() -> Callable[[Coroutine[Any, Any, T]], T]:
    if sys.implementation.name == "cpython":
        try:
            import uvloop  # type: ignore[import-not-found, unused-ignore]  # noqa: PLC0415
        except ImportError:
            pass
        else:
            try:
                return uvloop.run  # type: ignore[no-any-return, unused-ignore]
            except AttributeError:
                uvloop.install()
                return asyncio.run

        try:
            import winloop  # type: ignore[import-not-found, unused-ignore]  # noqa: PLC0415
        except ImportError:
            pass
        else:
            try:
                return winloop.run  # type: ignore[no-any-return, unused-ignore]
            except AttributeError:
                winloop.install()
                return asyncio.run
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.run


async def main() -> None:
    from . import bot, db  # noqa: PLC0415

    await db.init_db()
    await bot.bot.run_polling()


if __name__ == "__main__":
    _logs_listener.start()
    try:
        get_async_run()(main())
    finally:
        _logs_listener.stop()
