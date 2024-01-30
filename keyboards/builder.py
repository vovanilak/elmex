from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup

def reply_builder(names):
    builder = ReplyKeyboardBuilder()
    for i in names:
        builder.button(text=i)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)