from typing import Any

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramForbiddenError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Bot.Database import Channel, User


async def is_bot_admin_in_chat(bot: Bot, chat_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        return member.status == ChatMemberStatus.ADMINISTRATOR
    except TelegramForbiddenError:
        return False


async def notify_user_bot_removed(
    bot: Bot, chat_id: int, chat_title: Any, chat_type: str, session: AsyncSession
) -> None:
    try:
        channel_data = await session.scalar(
            select(Channel).where(Channel.Channel_id == chat_id)
        )
        user = await session.scalar(select(User).where(User.Id == channel_data.Adder))
        await bot.send_message(
            chat_id=user.Telegram_id,
            text=(
                f"❌ Бот был удалён из канала:\n"
                f"<b>{chat_title}</b>\n"
                f"ID: <code>{chat_title}</code>\n"
                f"Тип: <code>{chat_type}</code>"
            ),
            parse_mode="HTML",
        )
        await session.delete(channel_data)
    except TelegramForbiddenError:
        return


async def notify_user_bot_added(
    bot: Bot,
    user_id: int,
    chat_id: int,
    chat_title: Any,
    chat_type: str,
    is_admin: bool,
    session: AsyncSession,
) -> None:
    user = await session.scalar(select(User).where(User.Telegram_id == user_id))
    if is_admin:
        message = (
            f"✅ Бот добавлен в канал:\n"
            f"<b>{chat_title}</b>\n"
            f"ID: <code>{chat_id}</code>\n"
            f"Тип: <code>{chat_type}</code>\n\n"
            f"Бот <b>имеет права администратора</b> ✅"
        )
    else:
        message = (
            f"⚠️ Бот добавлен в канал:\n"
            f"<b>{chat_title}</b>\n"
            f"ID: <code>{chat_id}</code>\n"
            f"Тип: <code>{chat_type}</code>\n\n"
            f"❗ <b>Бот не является администратором</b>.\n"
            f"Пожалуйста, назначьте его админом, иначе он не сможет работать."
        )

    try:
        new_channel = Channel(
            Channel_id=chat_id, Channel_name=chat_title, Adder=user.Id
        )
        await bot.send_message(chat_id=user_id, text=message, parse_mode="HTML")
        session.add(new_channel)
    except TelegramForbiddenError:
        return
