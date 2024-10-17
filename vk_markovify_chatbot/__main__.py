from __future__ import annotations

import asyncio
import logging
import sys
from typing import TYPE_CHECKING

import rich.traceback
from rich.console import Console
from rich.logging import RichHandler

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


def configure_logging() -> None:
    console = Console()
    rich.traceback.install(
        console=console, width=None, extra_lines=0, word_wrap=True
    )
    logging.basicConfig(
        format="%(message)s",
        datefmt=logging.Formatter.default_time_format,
        level=logging.INFO,
        handlers=(
            RichHandler(
                console=console,
                omit_repeated_times=False,
                show_path=False,
                rich_tracebacks=True,
                tracebacks_extra_lines=0,
            ),
        ),
        force=True,
    )


async def main() -> None:
    configure_logging()

    from . import bot, db  # noqa: PLC0415

    await db.init_db()
    await bot.bot.run_polling()


if __name__ == "__main__":
    get_async_run()(main())
