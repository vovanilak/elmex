from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from dct import book, ru


main = ReplyKeyboardBuilder()
for k in book.keys():
    main.button(text=k)
main.adjust(3)

nomen = ReplyKeyboardBuilder()
for j in book["Номенклатура"].keys():
    nomen.button(text=j)
nomen.button(text=ru['back'])
nomen.adjust(2)

support = InlineKeyboardBuilder().button(text=ru['enter'],
                                         url=book["Технический вопрос"])

channel = InlineKeyboardBuilder().button(text=ru['enter'],
                                         url=book["ТГ-канал"])

def btn_download(url):
    if url:
        download = InlineKeyboardBuilder().button(
            text=ru['btn_download'],
            url=url
        )
        return download

def board_product(thing):
    prod = ReplyKeyboardBuilder()
    for p in book['Номенклатура'][thing].keys():
        prod.button(text=p)
    prod.button(text=ru['back'])
    prod.adjust(2)
    return prod

