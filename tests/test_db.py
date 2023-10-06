import sqlite3
import pytest
from app.database.db_crud import Db_Crud
import os
# Функция для создания и загрузки тестовой базы данных
TEST_DB_NAME = 'test_translation_history.db'
@pytest.fixture
def test_db():
    conn = sqlite3.connect(TEST_DB_NAME)  # Создаем тестовую базу данных
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


# Тесты для класса Db_Crud
def test_create_user_history(test_db):
    db = Db_Crud(TEST_DB_NAME)
    user_id = 1
    original_text = "Hello, world!"
    translated_text = "Привет, мир!"
    timestamp = "2023-09-29 12:00:00"

    db.create_user_histroy(user_id, original_text, translated_text, timestamp)
    history = db.get_translation_history(user_id)

    assert history[-1] == (user_id, original_text, translated_text, timestamp)


def test_get_translation_history(test_db):
    db = Db_Crud(TEST_DB_NAME)
    user_id = 1
    original_text = "Hello, world!"
    translated_text = "Привет, мир!"
    timestamp = "2023-09-29 12:00:00"

    # Создаем несколько записей
    db.create_user_histroy(user_id, original_text, translated_text, timestamp)
    db.create_user_histroy(user_id, "Another text", "Другой текст", "2023-09-30 12:00:00")

    history = db.get_translation_history(user_id)

    # Проверяем, что история содержит ожидаемое количество записей
    assert len(history) == 3

    # Проверяем, что последняя запись соответствует последней добавленной записи
    assert history[0] == (user_id, "Another text", "Другой текст", "2023-09-30 12:00:00")

@pytest.fixture(scope='session', autouse=True)
def cleanup_test_db():
    """
    Чистим тестовую бд
    """
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)