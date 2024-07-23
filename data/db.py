import sqlite3
import time
from datetime import datetime, timedelta
import pandas as pd

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


def get_stat():
    conn = sqlite3.connect('./data/messages.db')
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


def get_message_and_user_counts(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get current date and time
    now = datetime.fromtimestamp(1706722899.53854) #datetime.now()

    # Calculate the start times for today and the week
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_today - timedelta(days=start_of_today.weekday())

    # Convert datetime objects to timestamp strings for the query
    start_of_today_str = start_of_today.strftime('%Y-%m-%d %H:%M:%S')
    start_of_week_str = start_of_week.strftime('%Y-%m-%d %H:%M:%S')

    # Queries for today's messages and users
    cursor.execute("""
        SELECT COUNT(*) FROM messages 
        WHERE datetime(date) >= datetime(?)
    """, (start_of_today_str,))
    messages_today = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT user_id) FROM messages 
        WHERE datetime(date) >= datetime(?)
    """, (start_of_today_str,))
    users_today = cursor.fetchone()[0]

    # Queries for this week's messages and users
    cursor.execute("""
        SELECT COUNT(*) FROM messages 
        WHERE datetime(date) >= datetime(?)
    """, (start_of_week_str,))
    messages_week = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT user_id) FROM messages 
        WHERE datetime(date) >= datetime(?)
    """, (start_of_week_str,))
    users_week = cursor.fetchone()[0]
    # Close the database connection
    conn.close()
    return messages_today, users_today, messages_week, users_week

def stat(db_path):
    def read_table(db_path):
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query('SELECT * FROM messages', conn)
        conn.close()
        return df

    def clean_table(df):
        def date(x):
            if '.' in x:
                return pd.to_datetime(datetime.utcfromtimestamp(float(x)))
            elif '-' in x:
                return pd.to_datetime(x)
            else:
                return None
        df['date'] = df['date'].map(date)
        return df

    def graph_db(df):
        df.set_index('date', inplace=True)
        weekly= pd.DataFrame()
        weekly['Пользователи'] = df.drop_duplicates('user_id')['user_id'].resample('W').count()
        weekly['Сообщения'] = df.resample('W').count()['message_id']
        weekly.reset_index(inplace=True)
        weekly = weekly.rename(columns={'date': 'Неделя'})
        return weekly

    df = read_table(db_path)
    clean = clean_table(df)
    grouped = graph_db(clean)
    return grouped

if __name__ == "__main__":
    #create_db()
    #print(get_message_and_user_counts('./data/messages.db'))
    df = stat('./data/messages.db')
    print(df)
    #print(get_all())
    #print(clean_table('2024-01-30 00:00:00'))
