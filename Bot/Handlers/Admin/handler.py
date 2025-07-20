from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message, ChatMemberUpdated
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError

from Bot.Middleware import AdminMiddleware
from Bot.Keyboard.Admin import panel


class AdminHandler:
    def __init__(self, router: Router) -> None:
        self.router = router
        self._register_handlers()
        self.router.message.middleware(AdminMiddleware())

    def _register_handlers(self) -> None:
        self.router.message(Command("admin"))(self.admin_cmd)
        self.router.message(Command("resend"))(self.resned_cmd)
        self.router.my_chat_member()(self.added_update)

    async def admin_cmd(self, message: Message) -> None:
        await message.answer(text="Admin panel", reply_markup=panel())

    async def resned_cmd(self, message: Message) -> None:
        await message.send_copy(chat_id=message.chat.id)

    async def added_update(self, event: ChatMemberUpdated) -> None:
        chat = event.chat
        bot = event.bot
        user = event.from_user
        user_id = user.id

        if chat.type != ChatType.CHANNEL:
            return

        new_status = event.new_chat_member.status

        if new_status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=(
                        f"❌ Бот был удалён из канала:\n"
                        f"<b>{chat.title}</b>\n"
                        f"ID: <code>{chat.id}</code>\n"
                        f"Тип: <code>{chat.type}</code>"
                    ),
                    parse_mode="HTML",
                )
            except TelegramForbiddenError:
                print(f"❗ Не удалось отправить сообщение пользователю {user_id}")
            return

        try:
            member = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
            is_admin = member.status == ChatMemberStatus.ADMINISTRATOR
        except TelegramForbiddenError:
            is_admin = False

        if is_admin:
            message = (
                f"✅ Бот добавлен в канал:\n"
                f"<b>{chat.title}</b>\n"
                f"ID: <code>{chat.id}</code>\n"
                f"Тип: <code>{chat.type}</code>\n\n"
                f"Бот <b>имеет права администратора</b> ✅"
            )
        else:
            message = (
                f"⚠️ Бот добавлен в канал:\n"
                f"<b>{chat.title}</b>\n"
                f"ID: <code>{chat.id}</code>\n"
                f"Тип: <code>{chat.type}</code>\n\n"
                f"❗ <b>Бот не является администратором</b>.\n"
                f"Пожалуйста, назначьте его админом, иначе он не сможет работать."
            )

        try:
            await bot.send_message(chat_id=user_id, text=message, parse_mode="HTML")
        except TelegramForbiddenError:
            print(f"❗ Не удалось отправить сообщение пользователю {user_id}")
