from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Awaitable, Callable, Dict, Any
from Bot.config import settings


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Проверяем, что это сообщение (для других типов событий проверка не нужна)
        if not isinstance(event, Message):
            return await handler(event, data)

        # Проверяем права администратора
        if event.from_user.id in settings.ADMINS:
            return await handler(event, data)
        else:
            # Для не-админов прерываем выполнение
            await event.answer("⛔ У вас нет прав доступа к этой команде")
            return
