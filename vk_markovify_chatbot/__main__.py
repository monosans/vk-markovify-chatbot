from __future__ import annotations

import asyncio
import logging
import sys
from typing import Coroutine

from typing_extensions import Any, TypeVar

T = TypeVar("T")


def async_run(main: Coroutine[Any, Any, T]) -> T:
    if sys.implementation.name == "cpython":
        try:
            import uvloop  # type: ignore[import-not-found, unused-ignore]  # noqa: PLC0415
        except ImportError:
            pass
        else:
            if hasattr(uvloop, "run"):
                return uvloop.run(main)  # type: ignore[no-any-return, unused-ignore]
            uvloop.install()
            return asyncio.run(main)

        try:
            import winloop  # type: ignore[import-not-found, unused-ignore]  # noqa: PLC0415
        except ImportError:
            pass
        else:
            if hasattr(winloop, "run"):
                return winloop.run(main)  # type: ignore[no-any-return, unused-ignore]
            winloop.install()
            return asyncio.run(main)
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.run(main)


def configure_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt=logging.Formatter.default_time_format,
        level=logging.INFO,
        force=True,
    )


async def main() -> None:
    configure_logging()

    from . import bot, db  # noqa: PLC0415

    await db.init_db()
    await bot.bot.run_polling()


if __name__ == "__main__":
    async_run(main())
