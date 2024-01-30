import sqlite3
import datetime
import time

def create_db():
    conn = sqlite3.connect('../../messages.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date FLOAT,
        text TEXT
    )
    ''')

    conn.commit()
    conn.close()


def get_all():
    conn = sqlite3.connect('../../messages.db')
    cursor = conn.cursor()

    query = '''
            SELECT *
            FROM messages
            '''
    cursor.execute(query)
    return cursor.fetchall()


async def get_stat():
    conn = sqlite3.connect('../messages.db')
    cursor = conn.cursor()

    query_all = '''
                SELECT COUNT(DISTINCT user_id)
                FROM messages
                '''
    cursor.execute(query_all)
    number_of_all = cursor.fetchone()[0]

    today = datetime.datetime.now().date()
    midnight = datetime.datetime.combine(today, datetime.time())
    timestamp = int(time.mktime(midnight.timetuple()))

    query_messages_today = '''
            SELECT COUNT(*)
            FROM messages
            WHERE date >= ?
            '''

    cursor.execute(query_messages_today, (timestamp,))
    number_of_messages_today = cursor.fetchone()[0]
    query_users_today = '''
        SELECT COUNT(DISTINCT user_id)
        FROM messages
        WHERE date >= ?
        '''
    cursor.execute(query_users_today, (timestamp,))
    number_of_users_today = cursor.fetchone()[0]

    today = datetime.datetime.now().date()
    week_ago = today - datetime.timedelta(days=7)
    midnight_week_ago = datetime.datetime.combine(week_ago, datetime.time())
    timestamp_week_ago = int(time.mktime(midnight_week_ago.timetuple()))

    # Запрос для подсчета сообщений за последнюю неделю
    query_messages = '''
            SELECT COUNT(*)
            FROM messages
            WHERE date >= ?
            '''
    cursor.execute(query_messages, (timestamp_week_ago,))
    number_of_messages_week = cursor.fetchone()[0]
    query_users_week = '''
            SELECT COUNT(DISTINCT user_id)
            FROM messages
            WHERE date >= ?
            '''
    cursor.execute(query_users_week, (timestamp_week_ago,))
    number_of_users_week = cursor.fetchone()[0]

    return number_of_all, number_of_messages_today, number_of_users_today, number_of_messages_week, number_of_users_week


if __name__ == "__main__":
    #create_db()
    print(get_stat())
    print(get_all())
