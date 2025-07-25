from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message, ChatMemberUpdated
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError

from sqlalchemy.ext.asyncio import AsyncSession

from Bot.Middleware import AdminMiddleware
from Bot.Keyboard.Admin import panel
from Bot.Utils.ChannelUpdate import notify_user_bot_added, notify_user_bot_removed


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

    async def added_update(
        self, event: ChatMemberUpdated, session: AsyncSession
    ) -> None:
        chat = event.chat
        bot = event.bot
        user = event.from_user
        user_id = user.id
        chat_id = chat.id
        chat_title = chat.title
        chat_type = chat.type
        new_status = event.new_chat_member.status

        if new_status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            await notify_user_bot_removed(
                bot=bot,
                chat_id=chat_id,
                chat_title=chat_title,
                chat_type=chat_type,
                session=session,
            )
            return

        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
            is_admin = member.status == ChatMemberStatus.ADMINISTRATOR
        except TelegramForbiddenError:
            is_admin = False

        await notify_user_bot_added(
            bot=bot,
            user_id=user_id,
            chat_id=chat_id,
            chat_title=chat_title,
            chat_type=chat_type,
            is_admin=is_admin,
            session=session,
        )
