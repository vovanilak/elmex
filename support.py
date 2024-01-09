import asyncio
from aiogram.filters import Command
from aiogram.types import Message

import os
import logging
from aiogram import Bot, Dispatcher, filters, types, F
from dotenv import load_dotenv
from aiogram.methods import DeleteWebhook

load_dotenv()

TOKEN=os.getenv('TOKEN_INFO')
admin_chat_id = os.getenv('MYADMIN')
print(admin_chat_id)
bot = Bot(token=TOKEN)
dp = Dispatcher()


start_admin = ('Привет! Это чат администраторов поддержки Elmex. '
             'Сюда будут приходить сообщения от клиентов.'
             'Чтобы отправить ответ пользователя непосредственно ответить '
             'на конкретное сообщение (свайп влево)')
start_client = ('Здравствуйте! Это техподдержка Elmex '
                'Отправьте любой тектовый вопрос')

@dp.message(Command('start'))
async def cmd_start(msg: Message):
    if msg.chat.id == admin_chat_id:
        await msg.answer(start_admin)
    else:
        await msg.answer(start_client)

@dp.message(Command('getid'))
async def cmd_getid(msg: Message):
    await msg.answer(str(msg.chat.id))

@dp.message()
async def reply_message(msg: Message):
    print(msg.chat.id)
    if msg.chat.id == admin_chat_id:
        chat_to_send = msg.reply_to_message.forward_from.id
        if chat_to_send:
            answer = f'Сообщение от техподдержки:\n\n{msg.text}'
            await bot.send_message(text=answer, chat_id=chat_to_send)
            await msg.reply('Сообщение доставлено!')
        else:
            await msg.answer('Чтобы отправить сообщение клиенту, '
                             'ответьте на сообщение (свайп влево)')
    else:
        await bot.forward_message(from_chat_id=msg.chat.id,
                                  chat_id=admin_chat_id,
                                  message_id=msg.message_id)
        await msg.answer('Ожидайте ответа. Скоро ответим')


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())