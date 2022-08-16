#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import logging
import random
import re
import sys
from configparser import ConfigParser

import markovify
from aiofiles import open as aopen
from aiofiles import os as aos
from pydantic import BaseModel, Field
from vkbottle import VKAPIError
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import ChatActionRule, FromUserRule
from vkbottle_types.objects import MessagesMessageActionStatus


class Config(BaseModel):
    bot_token: str = Field(..., min_length=1)
    response_delay: float = Field(..., ge=0)
    response_chance: float = Field(..., gt=0, le=100)

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True


def get_config() -> Config:
    config_parser = ConfigParser()
    config_parser.read("config.ini", encoding="utf-8")
    cfg = config_parser["DEFAULT"]
    return Config(
        bot_token=cfg.get("BotToken"),
        response_delay=cfg.getfloat("ResponseDelay", 0),
        response_chance=cfg.getfloat("ResponseChance", 100),
    )


config = get_config()
bot = Bot(config.bot_token)
bot.loop_wrapper.on_startup.append(aos.makedirs("db", exist_ok=True))
tag_pattern = re.compile(r"\[(\w+?\d+?)\|.+?\]")


@bot.on.chat_message(  # type: ignore[misc]
    ChatActionRule(MessagesMessageActionStatus.CHAT_INVITE_USER.value)
)
async def invited(message: Message) -> None:
    """Приветствие при приглашении бота в беседу."""
    if (
        message.action is not None
        and message.group_id is not None
        and message.action.member_id == -message.group_id
    ):
        await message.answer(
            """Всем привет!
Для работы мне нужно выдать доступ к переписке или права администратора.
Для сброса базы данных используйте команды /сброс или /reset"""
        )


@bot.on.chat_message(text=["/сброс", "/reset"])  # type: ignore[misc]
async def reset(message: Message) -> None:
    """Сброс базы данных администратором беседы."""
    try:
        members = await message.ctx_api.messages.get_conversation_members(
            peer_id=message.peer_id
        )
    except VKAPIError[917]:
        await message.reply(
            "Не удалось проверить, являетесь ли вы администратором,"
            + " потому что я не администратор."
        )
        return
    admins = {member.member_id for member in members.items if member.is_admin}
    if message.from_id in admins:
        # Удаление базы данных беседы
        try:
            await aos.remove(f"db/{message.peer_id}.txt")
        except FileNotFoundError:
            pass

        reply = f"@id{message.from_id}, база данных успешно сброшена."
    else:
        reply = "Сбрасывать базу данных могут только администраторы."
    await message.reply(reply)


@bot.on.chat_message(FromUserRule())  # type: ignore[misc]
async def talk(message: Message) -> None:
    text = message.text
    file_name = f"db/{message.peer_id}.txt"

    if text:
        # Удаление пустых строк
        text = text.replace("\n\n", "\n")

        # Удаление пробела в начале строк
        text = text.replace("\n ", "\n")

        # Преобразование [id1|@durov] в @id1
        text = tag_pattern.sub(r"@\1", text)

        # Преобразование в нижний регистр
        text = text.lower()

        # Запись сообщения в историю беседы
        async with aopen(file_name, "a", encoding="utf-8") as f:
            await f.write(f"\n{text}")
    elif not await aos.path.exists(file_name):
        return

    if random.random() * 100 > config.response_chance:
        return

    # Задержка перед ответом
    await asyncio.sleep(config.response_delay)

    # Чтение истории беседы
    async with aopen(file_name, encoding="utf-8") as f:
        db = await f.read()
    db = db.strip().lower()

    # Генерация сообщения
    text_model = markovify.NewlineText(
        input_text=db, state_size=1, well_formed=False
    )
    sentence: str = text_model.make_sentence(tries=1000) or random.choice(
        db.splitlines()
    )

    await message.answer(sentence)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if sys.implementation.name == "cpython" and sys.platform in {
        "darwin",
        "linux",
    }:
        try:
            import uvloop
        except ImportError:
            pass
        else:
            uvloop.install()

    bot.run_forever()
