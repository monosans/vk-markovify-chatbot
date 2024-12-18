from __future__ import annotations

import asyncio
import logging
import stat

import aiosqlite
import platformdirs

from .fs import add_permission, create_or_fix_dir
from .text import clean_text

_logger = logging.getLogger(__name__)
DB_PATH = platformdirs.user_data_path("vk_markovify_chatbot") / "db.sqlite3"


def connect() -> aiosqlite.Connection:
    return aiosqlite.connect(DB_PATH, isolation_level=None)


async def init_db() -> None:
    if await asyncio.to_thread(DB_PATH.is_file):
        await asyncio.to_thread(
            add_permission, DB_PATH, stat.S_IRUSR | stat.S_IWUSR
        )
    elif await asyncio.to_thread(DB_PATH.exists):
        msg = f"{DB_PATH} must be a file"
        raise ValueError(msg)
    else:
        await asyncio.to_thread(
            create_or_fix_dir,
            DB_PATH.parent,
            permission=stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR,
        )
    sql = """\
        CREATE TABLE IF NOT EXISTS
            history (peer_id INTEGER NOT NULL, message TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS ix_history_peer_id ON history (peer_id);\
    """
    async with connect() as cn, cn.executescript(sql):
        pass
    _logger.info("The database is stored in %s", DB_PATH)


async def get_history(*, peer_id: int) -> list[str]:
    sql = "SELECT message FROM history WHERE peer_id = ?"
    params = (peer_id,)
    async with connect() as cn, cn.execute(sql, params) as cursor:
        rows = await cursor.fetchall()
    return [row[0] for row in rows]


async def add_to_history(*, peer_id: int, message: str) -> None:
    message = clean_text(message)
    sql = "INSERT INTO history (peer_id, message) VALUES (?, ?)"
    params = (peer_id, message)
    async with connect() as cn, cn.execute(sql, params):
        pass


async def clean_history(*, peer_id: int) -> None:
    sql = "DELETE FROM history WHERE peer_id = ?"
    params = (peer_id,)
    async with connect() as cn, cn.execute(sql, params):
        pass
