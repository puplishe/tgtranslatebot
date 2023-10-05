import sqlite3

def create_db() -> None:
    conn = sqlite3.connect('translation_history.db')
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation_history (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            original_text TEXT,
            translated_text TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')


    conn.commit()
    conn.close()

def db_conn():
    conn = sqlite3.connect('translation_history')
    return conn