from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING

from aiohttp import TCPConnector
from vkbottle import API, AiohttpClient, VKAPIError
from vkbottle.bot import Bot
from vkbottle.dispatch.rules.base import ChatActionRule, FromUserRule
from vkbottle_types.objects import MessagesMessageActionStatus

from . import config, db, http
from .text import generate_text

if TYPE_CHECKING:
    from vkbottle.bot import Message

cfg = config.from_toml("config.toml")
bot = Bot(
    api=API(
        token=cfg.bot_token,
        http_client=AiohttpClient(
            connector=TCPConnector(ssl=http.SSL_CONTEXT),
            fallback_charset_resolver=http.fallback_charset_resolver,
        ),
    )
)


@bot.on.chat_message(
    ChatActionRule(MessagesMessageActionStatus.CHAT_INVITE_USER.value)
)
async def invited(message: Message) -> None:
    """Приветствие при приглашении бота в беседу."""
    if (
        message.action is not None
        and message.group_id is not None
        and message.action.member_id == -message.group_id
    ):
        await message.answer("""Всем привет!
Для работы мне нужно выдать доступ к переписке или права администратора.
Для сброса базы данных используйте команды /сброс или /reset.""")


@bot.on.chat_message(text=["/сброс", "/reset"])
async def reset(message: Message) -> None:
    """Сброс базы данных администратором беседы."""
    try:
        members = await message.ctx_api.messages.get_conversation_members(
            peer_id=message.peer_id
        )
    except VKAPIError[917]:
        await message.reply(
            "Не удалось проверить, являетесь ли вы администратором,"
            " потому что я не администратор."
        )
        return
    admins = {member.member_id for member in members.items if member.is_admin}
    if message.from_id in admins:
        await db.clean_history(peer_id=message.peer_id)
        reply = f"@id{message.from_id}, база данных успешно сброшена."
    else:
        reply = "Сбрасывать базу данных могут только администраторы."
    await message.reply(reply)


@bot.on.chat_message(FromUserRule())
async def talk(message: Message) -> None:
    if message.text:
        await db.add_to_history(peer_id=message.peer_id, message=message.text)

    if random.random() * 100 > cfg.response_chance:
        return

    history = await db.get_history(peer_id=message.peer_id)
    response = generate_text(history=history)
    await asyncio.sleep(cfg.response_delay)
    await message.answer(response)
