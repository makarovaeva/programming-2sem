# tests/lab4/conftest.py
import sys
import tempfile
from pathlib import Path

import pytest

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lab4' / 'app'))

from lab4.app.database import DataBase


@pytest.fixture(scope="session")
def test_db_path():
    """Создаёт временную директорию и путь к тестовой БД"""
    # Используем временную директорию из tempfile (более надёжно)
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test_library.db"

    yield str(db_path)

    # После тестов удаляем временную директорию
    try:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass


@pytest.fixture
def db_session(test_db_path, monkeypatch):
    """Создаёт экземпляр DataBase с тестовой БД"""
    # Подменяем переменную окружения
    monkeypatch.setenv("DB_PATH", test_db_path)

    # Создаём новую БД
    db = DataBase()

    # Очищаем БД перед каждым тестом
    for table in reversed(DataBase.Base.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    yield db

    # Закрываем сессию
    db.close()

    # Закрываем engine (если есть метод dispose)
    if hasattr(DataBase, 'engine') and hasattr(DataBase.engine, 'dispose'):
        DataBase.engine.dispose()


@pytest.fixture
def sample_user(db_session):
    """Создаёт тестового пользователя"""
    db_session.add_user("Иван Петров", "ivan@example.com")
    return db_session.get_user(1)


@pytest.fixture
def sample_book(db_session):
    """Создаёт тестовую книгу"""
    db_session.add_book("Война и мир", "Лев Толстой", 3)
    return db_session.get_book(1)


@pytest.fixture
def sample_booking(db_session, sample_user, sample_book):
    """Создаёт тестовое бронирование"""
    db_session.add_booking(sample_user, sample_book)
    return db_session.get_booking(1)
