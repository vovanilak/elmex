import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('./data/messages.db')
cursor = conn.cursor()

# Update the date column values to timestamp format where the date is in 'YYYY-MM-DD' format
cursor.execute("""
    UPDATE messages
    SET date = DATETIME(date || ' 00:00:00')
    WHERE LENGTH(date) = 10
""")

# Commit the changes
conn.commit()

# Close the database connection
conn.close()
