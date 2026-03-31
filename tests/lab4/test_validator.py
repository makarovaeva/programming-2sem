# tests/test_validator.py
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))
from lab4.app.validator import Validator


class TestUserValidator:
    """Тесты валидации пользователя"""

    def test_valid_user(self, db_session):
        """Тест валидного пользователя"""
        # Создаем валидного пользователя
        Validator.is_user_valid("Иван Петров", "ivan@example.com", [])
        # Если нет исключения - тест пройден

    def test_user_empty_name(self, db_session):
        """Тест пользователя с пустым именем"""
        with pytest.raises(ValueError) as exc_info:
            Validator.is_user_valid("", "ivan@example.com", [])
        assert "не удалось" in str(exc_info.value)

    def test_user_none_name(self, db_session):
        """Тест пользователя с None в имени"""
        with pytest.raises(ValueError) as exc_info:
            Validator.is_user_valid(None, "ivan@example.com", [])
        assert "не null" in str(exc_info.value)

    def test_user_duplicate_email(self, db_session):
        """Тест пользователя с дублирующимся email"""

        # Создаем существующего пользователя
        class MockUser:
            email = "existing@example.com"

        existing_users = [MockUser()]

        with pytest.raises(ValueError) as exc_info:
            Validator.is_user_valid("Иван", "existing@example.com", existing_users)
        assert "уже существует" in str(exc_info.value)

    def test_user_invalid_email_type(self, db_session):
        """Тест пользователя с email не строкового типа"""
        with pytest.raises(ValueError) as exc_info:
            Validator.is_user_valid("Иван", 12345, [])
        assert "строками" in str(exc_info.value)


class TestBookValidator:
    """Тесты валидации книги"""

    def test_valid_book(self):
        """Тест валидной книги"""
        Validator.is_book_valid("Война и мир", "Лев Толстой", 5)
        # Если нет исключения - тест пройден

    def test_book_empty_title(self):
        """Тест книги с пустым названием"""
        with pytest.raises(ValueError) as exc_info:
            Validator.is_book_valid("", "Лев Толстой", 5)
        assert "не удалось" in str(exc_info.value)

    def test_book_none_author(self):
        """Тест книги с None в авторе"""
        with pytest.raises(ValueError) as exc_info:
            Validator.is_book_valid("Война и мир", None, 5)
        assert "не null" in str(exc_info.value)

    def test_book_negative_copies(self):
        """Тест книги с отрицательным количеством копий"""
        with pytest.raises(ValueError) as exc_info:
            Validator.is_book_valid("Война и мир", "Лев Толстой", -5)
        assert "натуральным числом" in str(exc_info.value)

    def test_book_none_copies(self):
        """Тест книги с None в количестве копий (допустимо)"""
        # None допустимо для copies_available
        Validator.is_book_valid("Война и мир", "Лев Толстой", None)

    def test_book_invalid_copies_type(self):
        """Тест книги с неправильным типом количества копий"""
        with pytest.raises(ValueError) as exc_info:
            Validator.is_book_valid("Война и мир", "Лев Толстой", "пять")
        assert "натуральным числом" in str(exc_info.value)
