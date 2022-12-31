from __future__ import annotations

import aiosqlite

from .text import clean_text

DB = "db.sqlite3"


async def init_db() -> None:
    sql = """CREATE TABLE IF NOT EXISTS
                history (peer_id INTEGER NOT NULL, message TEXT NOT NULL)"""
    async with aiosqlite.connect(DB) as con:
        await con.execute(sql)
        await con.commit()


async def get_history(peer_id: int) -> str:
    sql = "SELECT message FROM history WHERE peer_id = ?"
    params = (peer_id,)
    async with aiosqlite.connect("db.sqlite3") as con:
        res = await con.execute(sql, params)
        rows = await res.fetchall()
    return "\n".join(row[0] for row in rows)


async def add_to_history(peer_id: int, *, message: str) -> None:
    message = clean_text(message)
    sql = "INSERT INTO history (peer_id, message) VALUES (?, ?)"
    params = (peer_id, message)
    async with aiosqlite.connect(DB) as con:
        await con.execute(sql, params)
        await con.commit()


async def clean_history(peer_id: int) -> None:
    sql = "DELETE FROM history WHERE peer_id = ?"
    params = (peer_id,)
    async with aiosqlite.connect(DB) as con:
        await con.execute(sql, params)
        await con.commit()
