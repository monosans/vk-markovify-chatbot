from __future__ import annotations

from typing import List

import aiosqlite

from .text import clean_text


def connect() -> aiosqlite.Connection:
    return aiosqlite.connect("db.sqlite3", isolation_level=None)


async def init_db() -> None:
    sql = """
        CREATE TABLE IF NOT EXISTS
            history (peer_id INTEGER NOT NULL, message TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS ix_history_peer_id ON history (peer_id);
    """
    async with connect() as cn, cn.executescript(sql):
        pass


async def get_history(peer_id: int) -> List[str]:
    sql = "SELECT message FROM history WHERE peer_id = ?"
    params = (peer_id,)
    async with connect() as cn, cn.execute(sql, params) as cursor:
        rows = await cursor.fetchall()
    return [row[0] for row in rows]


async def add_to_history(peer_id: int, *, message: str) -> None:
    message = clean_text(message)
    sql = "INSERT INTO history (peer_id, message) VALUES (?, ?)"
    params = (peer_id, message)
    async with connect() as cn, cn.execute(sql, params):
        pass


async def clean_history(peer_id: int) -> None:
    sql = "DELETE FROM history WHERE peer_id = ?"
    params = (peer_id,)
    async with connect() as cn, cn.execute(sql, params):
        pass
