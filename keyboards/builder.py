from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup

def reply_builder(names):
    builder = ReplyKeyboardBuilder()
    for i in names:
        builder.button(text=i)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def inline(lst):
    builder = InlineKeyboardBuilder()
    for i in lst:
        builder.button(text=i, callback_data=i)
    return builder.adjust(1).as_markup()
