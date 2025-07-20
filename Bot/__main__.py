import asyncio
import colorlog
import logging

from aiogram import Bot, Dispatcher, Router
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from Bot.config import settings
from Bot.Handlers import Handler_Router
from Bot.Callbacks import Callback_Router
from Bot.Database import Base
from Bot.Middleware import DataBaseSessionMiddleware


class TelegramBot:
    def __init__(self, token: str, log_level: int = logging.INFO):
        self._setup_logging(log_level)
        self.logger = logging.getLogger(__name__)

        self.logger.info("Инициализация бота...")
        self.bot = Bot(token=token)
        self.dp = Dispatcher()

        self._engine = create_async_engine(settings.DATABASE_URL)
        self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)

        self._setup_middleware()
        self._setup_routers(Handler_Router(), Callback_Router())

        self.dp.startup.register(self._on_startup)
        self.dp.shutdown.register(self._on_shutdown)
        self.logger.info("Бот инициализирован")

    def _setup_logging(self, level: int):
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )

        logging.basicConfig(level=level, handlers=[handler])
        logging.getLogger("aiogram").setLevel(logging.DEBUG)
        logging.getLogger("asyncio").setLevel(logging.DEBUG)

    def _setup_routers(self, *routers: Router):
        """Добавление роутеров"""
        self.logger.debug(f"Добавление {len(routers)} роутеров...")
        for router in routers:
            self.dp.include_router(router=router)
        self.logger.debug("Роутеры добавлены")

    def _setup_middleware(self):
        """Настройка middleware"""
        self.logger.debug("Настройка middleware...")
        self.dp.message.middleware(DataBaseSessionMiddleware(self._session_maker))
        self.dp.callback_query.middleware(
            DataBaseSessionMiddleware(self._session_maker)
        )
        self.logger.debug("Middleware настроены")

    async def _on_startup(self) -> None:
        self.logger.debug("Bot starting up...")

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.logger.debug("Database tables created")

    async def _on_shutdown(self) -> None:
        self.logger.info("Shutting down, closing database connections...")
        await self._engine.dispose()
        self.logger.info("Database connections closed")

    async def run(self):
        """Запуск бота с обработкой ошибок"""
        self.logger.info("Запуск бота...")
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            self.logger.critical(f"Ошибка при работе бота: {e}", exc_info=True)
            raise
        finally:
            self.logger.info("Бот остановлен")
            await self.bot.session.close()


if __name__ == "__main__":
    bot = TelegramBot(settings.TOKEN, log_level=logging.INFO)
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("Бот остановлен по запросу пользователя")
