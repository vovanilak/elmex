from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_inline(text, url):
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=url)]
        ]
    )
    return btn
