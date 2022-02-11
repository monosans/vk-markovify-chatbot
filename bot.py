#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from asyncio import sleep
from os import mkdir
from random import choice, randint

from aiofiles import open
from aiofiles.os import remove
from aiofiles.ospath import exists
from markovify import NewlineText
from vkbottle import VKAPIError
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import ChatActionRule, FromUserRule

from config import BOT_TOKEN, RESPONSE_CHANCE, RESPONSE_DELAY

bot = Bot(BOT_TOKEN)
tag_pattern = re.compile(r"\[(id\d+?)\|.+?\]")
empty_line_pattern = re.compile(r"^\s+", flags=re.M)


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def invited(message: Message) -> None:
    """Приветствие при приглашении бота в беседу."""
    action = message.action
    group_id = message.group_id
    if not action or not group_id:
        return
    if action.member_id == -group_id:
        await message.answer(
            """Всем привет!
Для работы мне нужно выдать доступ к переписке или права администратора.
Для сброса базы данных используйте команды /сброс или /reset"""
        )


@bot.on.chat_message(text=["/сброс", "/reset"])
async def reset(message: Message) -> None:
    """Сброс базы данных администратором беседы."""
    peer_id = message.peer_id
    try:
        members = await message.ctx_api.messages.get_conversation_members(
            peer_id=peer_id
        )
    except VKAPIError[917]:
        await message.answer(
            "Не удалось проверить, являетесь ли вы администратором, "
            + "потому что я не администратор."
        )
        return
    admins = [member.member_id for member in members.items if member.is_admin]
    from_id = message.from_id
    if from_id in admins:

        # Удаление базы данных беседы
        try:
            await remove(f"db/{peer_id}.txt")
        except FileNotFoundError:
            pass

        await message.answer(f"@id{from_id}, база данных успешно сброшена.")
    else:
        await message.answer(
            "Сбрасывать базу данных могут только администраторы."
        )


@bot.on.chat_message(FromUserRule())
async def talk(message: Message) -> None:
    peer_id = message.peer_id
    text = message.text.lower()
    file_name = f"db/{peer_id}.txt"

    if text:
        # Удаление пустых строк и преобразование [id1|@durov] в @id1
        text = tag_pattern.sub(r"@\1", empty_line_pattern.sub("", text))

        # Запись сообщения в историю беседы
        async with open(file_name, "a") as f:
            await f.write(f"\n{text}")
    elif not await exists(file_name):
        return

    if randint(1, 100) > RESPONSE_CHANCE:
        return

    # Задержка перед ответом
    await sleep(RESPONSE_DELAY)

    # Чтение истории беседы
    async with open(file_name) as f:
        db = await f.read()
    db = db.strip().lower()

    # Генерация сообщения
    text_model = NewlineText(input_text=db, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000) or choice(db.splitlines())

    await message.answer(sentence)


if __name__ == "__main__":
    try:
        mkdir("db")
    except FileExistsError:
        pass
    bot.run_forever()
