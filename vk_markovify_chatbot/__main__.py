from __future__ import annotations

import asyncio
import logging
import sys


def install_uvloop() -> None:
    if sys.implementation.name == "cpython" and sys.platform in {
        "darwin",
        "linux",
    }:
        try:
            import uvloop
        except ImportError:
            pass
        else:
            asyncio.set_event_loop_policy(
                uvloop.EventLoopPolicy()  # type: ignore[attr-defined]
            )


def configure_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )


def main() -> None:
    install_uvloop()
    configure_logging()

    from .bot import bot

    bot.run_forever()


if __name__ == "__main__":
    main()
