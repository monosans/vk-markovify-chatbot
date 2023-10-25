from __future__ import annotations

import asyncio
import random

from vkbottle import VKAPIError
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import ChatActionRule, FromUserRule
from vkbottle_types.objects import MessagesMessageActionStatus

from . import config, db
from .text import generate_text

cfg = config.from_ini("config.ini")
bot = Bot(cfg.bot_token)
bot.loop_wrapper.on_startup.append(db.init_db())


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
        await message.answer(
            """Всем привет!
Для работы мне нужно выдать доступ к переписке или права администратора.
Для сброса базы данных используйте команды /сброс или /reset."""
        )


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
        await db.clean_history(message.peer_id)
        reply = f"@id{message.from_id}, база данных успешно сброшена."
    else:
        reply = "Сбрасывать базу данных могут только администраторы."
    await message.reply(reply)


@bot.on.chat_message(FromUserRule())
async def talk(message: Message) -> None:
    if message.text:
        await db.add_to_history(message.peer_id, message=message.text)

    if random.random() * 100 > cfg.response_chance:
        return

    history = await db.get_history(message.peer_id)
    response = generate_text(history)
    await asyncio.sleep(cfg.response_delay)
    await message.answer(response)
