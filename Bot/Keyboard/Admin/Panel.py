from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def panel() -> InlineKeyboardMarkup:
    stage1 = [
        InlineKeyboardButton(text="Добавить канал", url="https://www.youtube.com/"),
    ]
    stage2 = [
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
        InlineKeyboardButton(text="Каналы", callback_data="channel"),
    ]
    rows = [stage1, stage2]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
