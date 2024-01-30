import sqlite3

def create_db():
    conn = sqlite3.connect('../../messages.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT,
        text TEXT
    )
    ''')

    conn.commit()
    conn.close()

def get_stat():
    conn = sqlite3.connect('../../messages.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(message_id)
        FROM messages
        GROUP BY message_id
        ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
