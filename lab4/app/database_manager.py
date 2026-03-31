from typing import Type

from database import DataBase
from validator import Validator


def show_menu():
    """Показывает главное меню"""
    print(f"{'МЕНЮ':^30}")
    print("GET-ЗАПРОСЫ:")
    print("\t1. Получить всех пользователей.")
    print("\t2. Получить пользователя по идентификатору.")
    print("\t3. Получить все книги.")
    print("\t4. Получить книгу по идентификатору.")
    print("\t5. Получить все бронирования.")
    print("\t6. Получить бронирование по идентификатору.")
    print("POST-ЗАПРОСЫ:")
    print("\t7. Добавить пользователя.")
    print("\t8. Добавить книгу.")
    print("\t9. Создание бронирования.")
    print("PATCH-ЗАПРОСЫ:")
    print("\t10. Изменить email пользователя.")
    print("\t11. Изменить количество копий книги.")
    print("DELETE-ЗАПРОСЫ:")
    print("\t12. Удаление бронирования.")
    print("\t13. Удаление пользователя.")
    print("\t14. Удаление книги.")
    print("q. Выход.")


class DataBaseManager:
    """
    Класс для управления библиотечной системой через консольный интерфейс.

    Предоставляет интерактивное меню для выполнения CRUD операций с пользователями,
    книгами и бронированиями. Обрабатывает ввод пользователя, валидирует данные
    и вызывает соответствующие методы класса DataBase.

    Attributes:
        _db (DataBase): Экземпляр класса для работы с базой данных
        _running (bool): Флаг работы главного цикла программы
        _validator (Validator): Экземпляр класса для валидации входных данных
    """

    def __init__(self, db: DataBase) -> None:
        """
        Инициализирует менеджер базы данных.

        Args:
            db (DataBase): Экземпляр класса DataBase для работы с БД
        """
        self._db = db
        self._running = True
        self._validator = Validator()

    @property
    def db(self) -> DataBase:
        """
        Возвращает экземпляр базы данных.

        Returns:
            DataBase: Объект для работы с базой данных
        """
        return self._db

    @property
    def validator(self) -> Validator:
        """
        Возвращает экземпляр валидатора.

        Returns:
            Validator: Объект для валидации входных данных
        """
        return self._validator

    @property
    def running(self) -> bool:
        """
        Возвращает состояние работы программы.

        Returns:
            bool: True если программа запущена, False если завершена
        """
        return self._running

    @running.setter
    def running(self, state: bool) -> None:
        """
        Устанавливает состояние работы программы.

        Args:
            state (bool): Новое состояние (True - запущена, False - остановлена)
        """
        self._running = state

    def _add_user(self) -> str:
        """
        Запрашивает у пользователя данные для создания нового пользователя.

        Выполняет валидацию введённых данных через Validator.
        В случае успеха вызывает метод add_user из DataBase.

        Returns:
            str: Сообщение о результате операции (успех или ошибка валидации)
        """
        name = input("\nВведите имя пользователя: ")
        email = input("\nВведите email: ")
        try:
            self.validator.is_user_valid(name, email, self.db.get_users())
        except ValueError as e:
            return str(e)
        return self.db.add_user(name, email)

    def _add_book(self) -> str:
        """
        Запрашивает у пользователя данные для добавления новой книги.

        Выполняет валидацию введённых данных через Validator.
        Количество копий опционально (если не указано, устанавливается None).

        Returns:
            str: Сообщение о результате операции (успех или ошибка валидации)
        """
        title = input("\nВведите название книги: ")
        author = input("\nВведите имя автора: ")
        try:
            copies_available = int(input("\nВведите количество доступных копий: "))
        except ValueError:
            copies_available = None
        try:
            self.validator.is_book_valid(title, author, copies_available)
        except ValueError as e:
            return str(e)
        return self.db.add_book(title, author, copies_available)

    def _get_user(self) -> Type[DataBase.User] | str:
        """
        Запрашивает ID пользователя и возвращает его из базы данных.

        Обрабатывает некорректный ввод (не число) и случай, когда пользователь не найден.

        Returns:
            Type[DataBase.User] | str: Объект пользователя или сообщение об ошибке,
                        если пользователь не найден или введён некорректный ID
        """
        try:
            user_id = int(input("\nВведите идентификатор пользователя: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.")
            return self._get_user()
        user = self.db.get_user(user_id)
        if user is None:
            return f"Пользователь с идентификатором: {user_id} не существует."
        return user

    def _get_book(self) -> Type[DataBase.Book] | str:
        """
        Запрашивает ID книги и возвращает её из базы данных.

        Обрабатывает некорректный ввод (не число) и случай, когда книга не найдена.

        Returns:
            Type[DataBase.Book] | str: Объект книги или сообщение об ошибке,
                        если книга не найдена или введён некорректный ID
        """
        try:
            book_id = int(input("\nВведите идентификатор книги: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.")
            return self._get_book()
        book = self.db.get_book(book_id)
        if book is None:
            return f"Книга с идентификатором: {book_id} не существует"
        return book

    def _get_booking(self) -> Type[DataBase.Booking] | str:
        """
        Запрашивает ID бронирования и возвращает его из базы данных.

        Обрабатывает некорректный ввод (не число) и случай, когда бронирование не найдено.

        Returns:
            Type[DataBase.Booking] | str: Объект бронирования или сообщение об ошибке,
                           если бронирование не найдено или введён некорректный ID
        """
        try:
            booking_id = int(input("\nВведите идентификатор бронирования: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.")
            return self._get_booking()
        booking = self.db.get_booking(booking_id)
        if booking is None:
            return f"Бронирования с идентификатором: {booking_id} не существует"
        return booking

    def _add_booking(self) -> str:
        """
        Создаёт новое бронирование.

        Запрашивает у пользователя ID пользователя и ID книги через методы _get_user() и _get_book(),
        затем вызывает метод add_booking из DataBase.

        Returns:
            str: Результат операции бронирования
        """
        user = self._get_user()
        if not isinstance(user, DataBase.User):
            return user
        book = self._get_book()
        if not isinstance(book, DataBase.Book):
            return book
        return self.db.add_booking(user, book)

    def _delete_booking(self) -> str:
        """
        Удаляет бронирование по его ID.

        Запрашивает ID бронирования у пользователя и вызывает метод delete_booking из DataBase.

        Returns:
            str: Результат операции удаления
        """
        try:
            booking_id = int(input("\nВведите идентификатор бронирования: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.")
            return self._delete_booking()
        return self.db.delete_booking(booking_id)

    def _delete_user(self) -> str:
        """
        Удаляет пользователя по его ID.

        Запрашивает ID пользователя у пользователя и вызывает метод delete_user из DataBase.

        Returns:
            str: Результат операции удаления
        """
        try:
            user_id = int(input("\nВведите идентификатор пользователя: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.")
            return self._delete_user()
        return self.db.delete_user(user_id)

    def _delete_book(self) -> str:
        """
        Удаляет книгу по её ID.

        Запрашивает ID книги у пользователя и вызывает метод delete_book из DataBase.

        Returns:
            str: Результат операции удаления
        """
        try:
            book_id = int(input("\nВведите идентификатор книги: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.")
            return self._delete_book()
        return self.db.delete_book(book_id)

    def _get_users(self) -> None:
        """
        Выводит список всех пользователей.

        Получает список пользователей из базы данных и выводит их на экран.
        Если пользователи не найдены, выводит соответствующее сообщение.
        """
        users = self.db.get_users()
        if not users:
            print("Пользователей не найдено.\n")
            return
        for user in users:
            print(user)

    def _get_books(self) -> None:
        """
        Выводит список всех книг.

        Получает список книг из базы данных и выводит их на экран.
        Если книги не найдены, выводит соответствующее сообщение.
        """
        books = self.db.get_books()
        if not books:
            print("Книг не найдено.\n")
            return
        for book in books:
            print(book)

    def _get_all_booking(self) -> None:
        """
        Выводит список всех бронирований.

        Получает список бронирований из базы данных и выводит их на экран.
        Если бронирования не найдены, выводит соответствующее сообщение.
        """
        booking = self.db.get_all_booking()
        if not booking:
            print("Бронирований не найдено.\n")
            return
        for item in booking:
            print(item)

    def _update_book_copies(self) -> str:
        """
        Обновляет количество доступных копий книги.

        Запрашивает ID книги и новое количество копий у пользователя,
        затем вызывает метод update_book_copies из DataBase.

        Returns:
            str: Результат операции обновления
        """
        try:
            book_id = int(input("\nВведите идентификатор книги: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.\n")
            return self._update_book_copies()
        try:
            copies_available = int(input("\nВведите количество доступных копий: "))
        except ValueError:
            copies_available = None
        return self.db.update_book_copies(book_id, copies_available)

    def _update_user_email(self) -> str:
        """
        Обновляет email адрес пользователя.

        Запрашивает ID пользователя и новый email,
        проверяет уникальность email среди существующих пользователей,
        затем вызывает метод update_user_email из DataBase.

        Returns:
            str: Результат операции обновления или сообщение об ошибке,
                 если email уже существует
        """
        try:
            user_id = int(input("\nВведите идентификатор пользователя: "))
        except ValueError:
            print("Идентификатор должен быть натуральным числом.")
            return self._update_user_email()
        email = input("\nВведите новый email: ")
        users = self.db.get_users()
        for user in users:
            if user.email == email:
                return "Ошибка: пользователь с этим email уже существует.\n"
        return self.db.update_user_email(user_id, email)

    def run(self) -> None:
        """
        Запускает главный цикл программы.

        Отображает меню, обрабатывает выбор пользователя и вызывает соответствующие методы.
        Цикл продолжается до тех пор, пока пользователь не выберет пункт 'q' (выход).

        Доступные опции:
            1-6: GET запросы (просмотр данных)
            7-9: POST запросы (добавление данных)
            10-11: PATCH запросы (обновление данных)
            12-14: DELETE запросы (удаление данных)
            q: Выход из программы

        При выборе 'q' закрывает соединение с базой данных и завершает работу.
        """
        while self.running:
            show_menu()
            choice = input("Ваш выбор: ").lower()

            if choice == "1":
                self._get_users()
            elif choice == "2":
                print(self._get_user())
            elif choice == "3":
                self._get_books()
            elif choice == "4":
                print(self._get_book())
            elif choice == "5":
                self._get_all_booking()
            elif choice == "6":
                print(self._get_booking())
            elif choice == "7":
                print(self._add_user())
            elif choice == "8":
                print(self._add_book())
            elif choice == "9":
                print(self._add_booking())
            elif choice == "10":
                print(self._update_user_email())
            elif choice == "11":
                print(self._update_book_copies())
            elif choice == "12":
                print(self._delete_booking())
            elif choice == "13":
                print(self._delete_user())
            elif choice == "14":
                print(self._delete_book())
            elif choice == "q":
                self.running = False
                self.db.close()
                print("\nЗавершение работы с БД")
            else:
                print("\nНеверный выбор. Повторите ввод.")
