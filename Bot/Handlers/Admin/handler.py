from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from Bot.Middleware import AdminMiddleware


class AdminHandler:
    def __init__(self, router: Router) -> None:
        self.router = router
        self._register_handlers()
        self.router.message.middleware(AdminMiddleware())

    def _register_handlers(self) -> None:
        self.router.message(Command("admin"))(self.admin_cmd)
        self.router.message(Command("resend"))(self.resned_cmd)

    async def admin_cmd(self, message: Message) -> None:
        await message.answer(text="Admin panel")

    async def resned_cmd(self, message: Message) -> None:
        await message.send_copy(chat_id=message.chat.id)
