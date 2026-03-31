import os
from datetime import datetime
from pathlib import Path
from typing import Type

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


def _get_engine():
    """
    Создаёт и возвращает engine для подключения к базе данных.

    Функция читает путь к БД из переменной окружения DB_PATH,
    или использует значение по умолчанию 'library.db'.

    Returns:
        Engine: Объект SQLAlchemy engine для работы с БД
    """
    base_dir = Path(__file__).resolve().parent.parent
    env_path = base_dir / '.env'
    load_dotenv(env_path)
    db_path = os.getenv('DB_PATH', 'library.db')
    engine = create_engine(f"sqlite:///{db_path}")
    return engine


class DataBase:
    """
    Основной класс для работы с библиотечной базой данных.

    Предоставляет CRUD операции для управления пользователями, книгами и бронированиями.

    Attributes:
        Base: Базовый класс SQLAlchemy для декларативного создания моделей
    """
    Base = declarative_base()

    def __init__(self):
        """
        Инициализирует подключение к базе данных и создаёт таблицы.

        Создаёт engine, sessionmaker и сессию для работы с БД.
        Если таблицы не существуют, они будут созданы автоматически.
        """
        self._engine = _get_engine()
        self._Session = sessionmaker(bind=self.engine)
        self._session = self._Session()

        DataBase.Base.metadata.create_all(self.engine)

    @property
    def session(self) -> sqlalchemy.orm.session:
        """
        Возвращает текущую сессию SQLAlchemy.

        Returns:
            Session: Объект сессии для выполнения запросов к БД
        """
        return self._session

    @property
    def engine(self) -> sqlalchemy.engine:
        """
        Возвращает engine подключения к базе данных.

        Returns:
            Engine: Объект SQLAlchemy engine
        """
        return self._engine

    def close(self):
        """
        Закрывает текущую сессию подключения к базе данных.

        Освобождает ресурсы, связанные с сессией.
        """
        self.session.close()

    class User(Base):
        """
        Модель пользователя библиотеки.

        Attributes:
            id (int): Уникальный идентификатор пользователя (первичный ключ)
            name (str): Имя пользователя, не может быть пустым
            email (str): Email пользователя, уникальный и не может быть пустым
            bookings (relationship): Связь с бронированиями пользователя
        """
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        email = Column(String, unique=True, nullable=False)

        bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")

        def _view_list_of_books(self):
            """
            Формирует строку со списком забронированных книг.

            Returns:
                str: Строка с названиями книг или сообщение об отсутствии книг
            """
            if not self.bookings:
                return "\tКниги не найдены."
            return "\n\t".join(booking.book.title for booking in self.bookings)

        def __repr__(self):
            """
            Строковое представление объекта пользователя.

            Returns:
                str: Отформатированная строка с информацией о пользователе
                     и его забронированных книгах
            """
            return (f"Пользователь {self.name}:\n\t"
                    f"id: {self.id}\n\t"
                    f"email: {self.email}\n"
                    f"Забронированные книги:\n\t{self._view_list_of_books()}\n")

    class Book(Base):
        """
        Модель книги в библиотеке.

        Attributes:
            id (int): Уникальный идентификатор книги (первичный ключ)
            title (str): Название книги, не может быть пустым
            author (str): Автор книги, не может быть пустым
            copies_available (int): Количество доступных копий книги
            bookings (relationship): Связь с бронированиями книги
        """
        __tablename__ = "books"
        id = Column(Integer, primary_key=True)
        title = Column(String, nullable=False)
        author = Column(String, nullable=False)
        copies_available = Column(Integer)

        bookings = relationship("Booking", back_populates="book", cascade="all, delete-orphan")

        def __repr__(self):
            """
            Строковое представление объекта книги.

            Returns:
                str: Отформатированная строка с информацией о книге
            """
            return (f"\nКнига №{self.id}:\n\t"
                    f"Название: {self.title}\n\t"
                    f"Автор: {self.author}\n\t"
                    f"Количество доступных копий: {self.copies_available if self.copies_available is not None else 'не указано'}")

    class Booking(Base):
        """
        Модель бронирования книги пользователем.

        Attributes:
            id (int): Уникальный идентификатор бронирования (первичный ключ)
            user_id (int): Внешний ключ на пользователя
            book_id (int): Внешний ключ на книгу
            booking_date (datetime): Дата и время создания бронирования
            user (relationship): Связь с пользователем
            book (relationship): Связь с книгой
        """
        __tablename__ = "booking"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
        book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
        booking_date = Column(DateTime)

        user = relationship("User", back_populates="bookings")
        book = relationship("Book", back_populates="bookings")

        def __repr__(self):
            """
            Строковое представление объекта бронирования.

            Returns:
                str: Отформатированная строка с информацией о бронировании
            """
            return (f"\nБронирование №{self.id}:"
                    f"\n\tКнига: {self.book.title}"
                    f"\n\tЗабронирована пользователем: {self.user.name}"
                    f"\n\tДата бронирования: {self.booking_date}")

    def add_book(self, title: str, author: str, copies_available: int) -> str:
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги
            author (str): Автор книги
            copies_available (int): Количество доступных копий

        Returns:
            str: Сообщение о результате операции
        """
        book = DataBase.Book(title=title, author=author, copies_available=copies_available)
        self.session.add(book)
        self.session.commit()
        return f"Книга {title} успешно добавлена.\n"

    def add_user(self, name: str, email: str) -> str:
        """
        Добавляет нового пользователя в систему.

        Args:
            name (str): Имя пользователя
            email (str): Email пользователя (должен быть уникальным)

        Returns:
            str: Сообщение о результате операции
        """
        user = DataBase.User(name=name, email=email)
        self.session.add(user)
        self.session.commit()
        return f"Пользователь {name} успешно добавлен.\n"

    def add_booking(self, user: User, book: Book) -> str:
        """
        Создаёт бронирование книги для пользователя.

        Args:
            user (User): Объект пользователя
            book (Book): Объект книги

        Returns:
            str: Сообщение о результате операции
        """
        user = self.session.merge(user)
        book = self.session.merge(book)
        if book.copies_available is None or book.copies_available == 0:
            return f"Книга {book.title} не имеет доступных копий для бронирования."
        booking = DataBase.Booking(user=user, book=book, booking_date=datetime.today())
        book.copies_available -= 1
        self.session.add(booking)
        self.session.commit()
        return f"Пользователь {user.name} забронировал книгу {book.title}\n"

    def get_users(self) -> list[Type[User]]:
        """
        Получает список всех пользователей.

        Returns:
            list[Type[User]]: Список объектов User
        """
        return self.session.query(DataBase.User).all()

    def get_books(self) -> list[Type[Book]]:
        """
        Получает список всех книг.

        Returns:
            list[Type[Book]]: Список объектов Book
        """
        return self.session.query(DataBase.Book).all()

    def get_all_booking(self) -> list[Type[Booking]]:
        """
        Получает список всех бронирований.

        Returns:
            list[Type[Booking]]: Список объектов Booking
        """
        return self.session.query(DataBase.Booking).all()

    def get_user(self, user_id: int) -> Type[User] | None:
        """
        Получает пользователя по его идентификатору.

        Args:
            user_id (int): ID пользователя

        Returns:
            Type[User] | None: Объект User или None, если пользователь не найден
        """
        return self.session.query(DataBase.User).filter_by(id=user_id).first()

    def get_book(self, book_id: int) -> Type[Book] | None:
        """
        Получает книгу по её идентификатору.

        Args:
            book_id (int): ID книги

        Returns:
            Type[Book] | None: Объект Book или None, если книга не найдена
        """
        return self.session.query(DataBase.Book).filter_by(id=book_id).first()

    def get_booking(self, booking_id: int) -> Type[Booking] | None:
        """
        Получает бронирование по его идентификатору.

        Args:
            booking_id (int): ID бронирования

        Returns:
            Type[Booking] | None: Объект Booking или None, если бронирование не найдено
        """
        return self.session.query(DataBase.Booking).filter_by(id=booking_id).first()

    def update_book_copies(self, book_id: int, new_copies: int) -> str:
        """
        Обновляет количество доступных копий книги.

        Args:
            book_id (int): ID книги
            new_copies (int): Новое количество копий

        Returns:
            str: Сообщение о результате операции
        """
        if new_copies is None:
            return f"Не удалось обновить количество копий.\n"
        book = self.get_book(book_id)
        if book:
            book.copies_available = new_copies
            self.session.commit()
            return f"Количество копий книги '{book.title}' обновлено: {new_copies}\n"
        return f"Книга с ID {book_id} не найдена\n"

    def update_user_email(self, user_id: int, new_email: str) -> str:
        """
        Обновляет email адрес пользователя.

        Args:
            user_id (int): ID пользователя
            new_email (str): Новый email адрес

        Returns:
            str: Сообщение о результате операции
        """
        user = self.get_user(user_id)
        if user:
            user.email = new_email
            self.session.commit()
            return f"Email пользователя {user.name} обновлен\n"
        return f"Пользователь с ID {user_id} не найден\n"

    def delete_booking(self, booking_id: int) -> str:
        """
        Удаляет бронирование и возвращает книгу в библиотеку.

        Args:
            booking_id (int): ID бронирования

        Returns:
            str: Сообщение о результате операции
        """
        booking = self.get_booking(booking_id)
        if booking is None:
            return f"Бронирования с идентификатором {booking_id} не существует.\n"
        book_name = booking.book.title
        user_name = booking.user.name
        booking.book.copies_available += 1
        self.session.delete(booking)
        self.session.commit()
        return f"Бронирование книги {book_name} пользователем {user_name} успешно удалено.\n"

    def delete_user(self, user_id: int) -> str:
        """
        Удаляет пользователя из системы.

        Args:
            user_id (int): ID пользователя

        Returns:
            str: Сообщение о результате операции
        """
        user = self.get_user(user_id)
        if user is None:
            return f"Пользователь с ID {user_id} не найден\n"
        name = user.name
        self.session.delete(user)
        self.session.commit()
        return f"Пользователь {name} удален\n"

    def delete_book(self, book_id: int) -> str:
        """
        Удаляет книгу из библиотеки.

        Args:
            book_id (int): ID книги

        Returns:
            str: Сообщение о результате операции
        """
        book = self.get_book(book_id)
        if book is None:
            return f"Книга с ID {book_id} не найдена\n"
        title = book.title
        self.session.delete(book)
        self.session.commit()
        return f"Книга '{title}' удалена\n"