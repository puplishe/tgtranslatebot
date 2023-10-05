import sqlite3
from .db_conn import db_conn

class Db_Crud():
    def __init__(self) -> None:
        pass

    def db_conn(self):
        """
        Создает сессию бд
        """
        conn = sqlite3.connect('translation_history.db')
        return conn
    
    def create_user_histroy(self, user_id, original_text, translated, timestamp) -> None:
        """
        Создает историю запросов перевода
        """
        conn = self.db_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO translation_history (user_id, original_text, translated_text, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, original_text, translated, timestamp))
        
        conn.commit()
        conn.close()



    def get_translation_history(self, user_id) -> list:
        """
        Возвращает историю юзера, если user_id, либо историю всех юзеров, если user_id is None
        """
        conn = self.db_conn()
        cursor = conn.cursor()
        if user_id is None:
            cursor.execute('''
                SELECT id, user_id, original_text, translated_text, timestamp
                FROM translation_history
                ORDER BY timestamp DESC
            ''')
        else:
            cursor.execute('''
                SELECT id, user_id, original_text, translated_text, timestamp
                FROM translation_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
            ''', (user_id,))

        history = cursor.fetchall()
        
        conn.close()
        
        return history

    def get_user_id(self) -> list:
        """
        Возвращает все существующие user_id
        """
        conn = self.db_conn()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT user_id
        FROM translation_history
        ORDER BY user_id DESC
        ''')
        users_ids = cursor.fetchall()
        conn.close()
        return users_ids


