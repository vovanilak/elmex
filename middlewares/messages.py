from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
import sqlite3
import datetime


class DbLogMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler,
                       event: types.Message,
                       data):
        conn = sqlite3.connect('./data/messages.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO messages (message_id, user_id, date, text)
        VALUES (?, ?, ?, ?)
        ''', (event.message_id, event.from_user.id, datetime.datetime.now().timestamp(), event.text))

        conn.commit()
        conn.close()
        return await handler(event, data)
