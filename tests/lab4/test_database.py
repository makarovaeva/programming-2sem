# tests/lab4/test_database.py


class TestUserCRUD:
    """Тесты для операций с пользователями"""

    def test_add_user_success(self, db_session):
        """Тест успешного добавления пользователя"""
        result = db_session.add_user("Иван Петров", "ivan@example.com")

        assert "успешно добавлен" in result
        user = db_session.get_user(1)
        assert user is not None
        assert user.name == "Иван Петров"
        assert user.email == "ivan@example.com"

    def test_get_user_by_id(self, db_session):
        """Тест получения пользователя по ID"""
        db_session.add_user("Иван Петров", "ivan@example.com")
        user = db_session.get_user(1)

        assert user is not None
        assert user.id == 1
        assert user.name == "Иван Петров"

    def test_get_user_not_found(self, db_session):
        """Тест получения несуществующего пользователя"""
        user = db_session.get_user(999)
        assert user is None

    def test_get_all_users(self, db_session):
        """Тест получения всех пользователей"""
        db_session.add_user("Иван Петров", "ivan@example.com")
        db_session.add_user("Мария Сидорова", "maria@example.com")

        users = db_session.get_users()
        assert len(users) == 2
        names = [u.name for u in users]
        assert "Иван Петров" in names
        assert "Мария Сидорова" in names

    def test_update_user_email_success(self, db_session):
        """Тест успешного обновления email пользователя"""
        db_session.add_user("Иван Петров", "ivan@example.com")
        result = db_session.update_user_email(1, "newemail@example.com")

        assert "обновлен" in result
        user = db_session.get_user(1)
        assert user.email == "newemail@example.com"

    def test_delete_user_success(self, db_session):
        """Тест успешного удаления пользователя"""
        db_session.add_user("Иван Петров", "ivan@example.com")
        result = db_session.delete_user(1)

        assert "удален" in result
        user = db_session.get_user(1)
        assert user is None


class TestBookCRUD:
    """Тесты для операций с книгами"""

    def test_add_book_success(self, db_session):
        """Тест успешного добавления книги"""
        result = db_session.add_book("Война и мир", "Лев Толстой", 3)

        assert "успешно добавлена" in result
        book = db_session.get_book(1)
        assert book is not None
        assert book.title == "Война и мир"
        assert book.author == "Лев Толстой"
        assert book.copies_available == 3

    def test_get_book_by_id(self, db_session):
        """Тест получения книги по ID"""
        db_session.add_book("Война и мир", "Лев Толстой", 3)
        book = db_session.get_book(1)

        assert book is not None
        assert book.id == 1

    def test_update_book_copies_success(self, db_session):
        """Тест обновления количества копий"""
        db_session.add_book("Война и мир", "Лев Толстой", 3)
        result = db_session.update_book_copies(1, 10)

        assert "обновлено" in result
        book = db_session.get_book(1)
        assert book.copies_available == 10

    def test_delete_book_success(self, db_session):
        """Тест удаления книги"""
        db_session.add_book("Война и мир", "Лев Толстой", 3)
        result = db_session.delete_book(1)

        assert "удалена" in result
        book = db_session.get_book(1)
        assert book is None


class TestBookingCRUD:
    """Тесты для операций с бронированиями"""

    def test_add_booking_success(self, db_session, sample_user, sample_book):
        """Тест успешного создания бронирования"""
        result = db_session.add_booking(sample_user, sample_book)

        assert "забронировал" in result
        bookings = db_session.get_all_booking()
        assert len(bookings) == 1

        # Проверяем уменьшение количества копий
        updated_book = db_session.get_book(1)
        assert updated_book.copies_available == 2

    def test_add_booking_unavailable_book(self, db_session):
        """Тест бронирования недоступной книги"""
        db_session.add_user("Иван Петров", "ivan@example.com")
        db_session.add_book("Война и мир", "Толстой", 0)

        user = db_session.get_user(1)
        book = db_session.get_book(1)

        result = db_session.add_booking(user, book)

        assert "не имеет доступных копий" in result
        assert len(db_session.get_all_booking()) == 0

    def test_delete_booking_success(self, db_session, sample_booking):
        """Тест удаления бронирования"""
        book = db_session.get_book(1)
        initial_copies = book.copies_available

        result = db_session.delete_booking(1)

        assert "успешно удалено" in result
        assert db_session.get_booking(1) is None

        # Проверяем возврат копии
        updated_book = db_session.get_book(1)
        assert updated_book.copies_available == initial_copies + 1

    def test_cascade_delete_user(self, db_session):
        """Тест каскадного удаления при удалении пользователя"""
        # Создаём пользователя и книгу
        db_session.add_user("Иван Петров", "ivan@example.com")
        db_session.add_book("Война и мир", "Толстой", 3)

        user = db_session.get_user(1)
        book = db_session.get_book(1)

        # Создаём бронирование
        db_session.add_booking(user, book)

        # Удаляем пользователя
        db_session.delete_user(1)

        # Проверяем
        assert db_session.get_user(1) is None
        assert db_session.get_book(1) is not None  # Книга осталась
        assert len(db_session.get_all_booking()) == 0  # Бронирование удалилось

    def test_cascade_delete_book(self, db_session):
        """Тест каскадного удаления при удалении книги"""
        # Создаём пользователя и книгу
        db_session.add_user("Иван Петров", "ivan@example.com")
        db_session.add_book("Война и мир", "Толстой", 3)

        user = db_session.get_user(1)
        book = db_session.get_book(1)

        # Создаём бронирование
        db_session.add_booking(user, book)

        # Удаляем книгу
        db_session.delete_book(1)

        # Проверяем
        assert db_session.get_book(1) is None
        assert db_session.get_user(1) is not None  # Пользователь остался
        assert len(db_session.get_all_booking()) == 0  # Бронирование удалилось
