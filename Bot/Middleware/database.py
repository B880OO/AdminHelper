from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy.ext.asyncio import async_sessionmaker


class DataBaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker) -> None:
        """Initialize with session pool."""
        self._session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        """Inject session into handler data and manage transaction automatically."""
        async with self._session_pool() as session:
            async with session.begin():
                data["session"] = session
                return await handler(event, data)
