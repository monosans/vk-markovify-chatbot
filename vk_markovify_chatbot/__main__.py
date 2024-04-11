from __future__ import annotations

import asyncio
import logging
import sys


def set_event_loop_policy() -> None:
    if sys.implementation.name == "cpython":
        if sys.platform in {"cygwin", "win32"}:
            try:
                import winloop  # type: ignore[import-not-found]  # noqa: PLC0415
            except ImportError:
                pass
            else:
                try:
                    policy = winloop.EventLoopPolicy()
                except AttributeError:
                    policy = winloop.WinLoopPolicy()
                asyncio.set_event_loop_policy(policy)
                return
        elif sys.platform in {"darwin", "linux"}:
            try:
                import uvloop  # noqa: PLC0415
            except ImportError:
                pass
            else:
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                return
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def configure_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt=logging.Formatter.default_time_format,
        level=logging.INFO,
        force=True,
    )


def main() -> None:
    set_event_loop_policy()
    configure_logging()

    from .bot import bot  # noqa: PLC0415

    bot.run_forever()


if __name__ == "__main__":
    main()
