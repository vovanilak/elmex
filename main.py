import asyncio
import json
import os
from dotenv import load_dotenv
import logging
import json

from aiogram import Bot, Dispatcher, types, filters, F, Router
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.methods import DeleteWebhook
from dct import *
import utils
import board
from aiogram.types import Message, FSInputFile

load_dotenv()
TOKEN=os.getenv('TOKEN_INFO')
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
users = {}


class Menu(StatesGroup):
    start = State()
    layer2 = State()
    nomen = State()
    product = State()

@router.message(or_f(or_f(StateFilter(default_state),
                     StateFilter(Menu.start)),
                Command('start')))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Menu.layer2)
    await message.answer(ru['start'],
                         reply_markup=board.main.as_markup(resize_keyboard=True))

@router.message(StateFilter(Menu.layer2),
                F.text.in_(book.keys()))
async def info(message: Message, state: FSMContext):
    txt = message.text
    kys = list(book.keys())
    if txt == kys[4]:
        await state.set_state(Menu.nomen)
        await message.answer(text=ru['nomen'],
                             reply_markup=board.nomen.as_markup(resize_keyboard=True))
    elif txt == kys[1]:
        await message.answer(text=ru['support'],
                             reply_markup=board.support.as_markup())
    elif txt == kys[0]:
        await message.answer(text=ru['channel'],
                             reply_markup=board.channel.as_markup())
    else:
        await message.answer(text=book[txt])


@router.message(StateFilter(Menu.layer2))
async def error_info(message: Message, state: FSMContext):
    await message.answer(ru['no_btn'],
                         reply_markup=board.main)

@router.message(
    StateFilter(Menu.nomen),
    F.text.in_(book["Номенклатура"])
)
async def nom(message: Message, state: FSMContext):
    global users
    txt = message.text
    users[message.from_user.id] = txt
    thing = book['Номенклатура'][txt]
    if len(thing) > 1:
        await state.set_state(Menu.product)
        await message.answer(
            text=ru['mes_which_type'],
            reply_markup=board.board_product(txt).as_markup(resize_keyboard=True))
    else:
        if len(thing[txt]['photo']) > 1:
            await message.answer_media_group(
                media=utils.get_album(txt, txt).build(),
            )
            if thing[txt]['url']:
                await message.answer(
                    text=ru['mes_download'],
                    reply_markup=board.btn_download(thing[txt]['url']).as_markup()
                )
        else:
            thing = thing[txt]
            if thing['url']:
                await message.answer_photo(
                    photo=FSInputFile(path=f"data/{thing['photo'][0]}.PNG"),
                    caption=thing["Описание"],
                    reply_markup=board.btn_download(thing['url']).as_markup()
                )
            else:
                await message.answer_photo(
                    photo=FSInputFile(path=f"data/{thing['photo'][0]}.PNG"),
                    caption=thing["Описание"]
                )

@router.message(
    StateFilter(Menu.nomen),
    F.text == ru['back']
)
async def back_to_main(message: Message,
                       state: FSMContext):
    await state.set_state(Menu.layer2)
    await message.answer(
        text=ru['mes_main'],
        reply_markup=board.main.as_markup(resize_keyboard=True)
    )

@router.message(StateFilter(Menu.nomen))
async def error_nomen(message: Message):
    await message.answer(text=ru['no_btn'],
                         reply_markup=board.nomen.as_markup(resize_keyboard=True))

@router.message(
    StateFilter(Menu.product),
    F.text.in_(utils.get_prod_in_type())
)
async def send_product(message: Message,
                       state: FSMContext):
    type = users[message.from_user.id]
    prod = message.text
    thing = book["Номенклатура"][type][prod]
    if len(thing['photo']) > 1:
        await message.answer_media_group(
            media=utils.get_album(type, prod).build(),
        )
        if thing['url']:
            await message.answer(
                text=ru['mes_download'],
                reply_markup=board.btn_download(thing['url']).as_markup()
            )
    else:
        if thing['url']:
            await message.answer_photo(
                photo=FSInputFile(path=f"data/{thing['photo'][0]}.PNG"),
                caption=thing["Описание"],
                reply_markup=board.btn_download(thing['url']).as_markup()
            )
        else:
            await message.answer_photo(
                photo=FSInputFile(path=f"data/{thing['photo'][0]}.PNG"),
                caption=thing["Описание"]
            )

@router.message(
    StateFilter(Menu.product),
    F.text == ru['back']
)
async def back_to_nomen(message: Message,
                        state: FSMContext):
    txt = users[message.from_user.id]
    await state.set_state(Menu.nomen)
    await message.answer(
        text=ru['nomen'],
        reply_markup=board.nomen.as_markup(resize_keyboard=True))

@router.message(StateFilter(Menu.product))
async def error_product(message: Message,
                        state: FSMContext):
    await message.answer(ru['error_product'])


@router.message()
async def error_main(message: Message, state: FSMContext):
    await state.set_state(Menu.layer2)
    await message.answer(ru['error_main'])
    await message.answer(
        text=ru['mes_main'],
        reply_markup=board.main.as_markup(resize_keyboard=True)
    )


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())