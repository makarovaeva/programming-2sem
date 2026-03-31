from typing import Any


class Validator:
    """
    Класс для валидации входных данных перед добавлением в базу данных.

    Содержит статические методы для проверки корректности данных пользователей и книг.
    """

    @staticmethod
    def is_user_valid(name: str, email: str, users: list[Any]) -> None:
        """
        Проверяет корректность данных пользователя перед добавлением.

        Выполняет следующие проверки:
            - Тип данных: name и email должны быть строками
            - Значение: name и email не могут быть пустыми строками
            - Значение: name и email не могут быть None
            - Уникальность: email не должен существовать в списке существующих пользователей

        Args:
            name (str): Имя пользователя для проверки
            email (str): Email пользователя для проверки
            users (list[Any]): Список существующих пользователей для проверки уникальности email

        Raises:
            ValueError: Если любая из проверок не пройдена.
                        Сообщение содержит подробное описание всех ошибок.
        """
        message = "Добавить пользователя не удалось.\n"
        is_valid = True
        if not isinstance(name, str) or not isinstance(email, str):
            message += "Ошибка: параметры должны быть строками.\n"
            is_valid = False
        if name == "" or email == "":
            message += "Ошибка: параметры не могут быть пустыми строками.\n"
            is_valid = False
        if name is None or email is None:
            message += "Ошибка: параметры должны быть не null.\n"
            is_valid = False
        for user in users:
            if user.email == email:
                message += "Ошибка: пользователь с этим email уже существует.\n"
                is_valid = False
                break
        if not is_valid:
            raise ValueError(message)

    @staticmethod
    def is_book_valid(title: str, author: str, copies_available: int) -> None:
        """
        Проверяет корректность данных книги перед добавлением.

        Выполняет следующие проверки:
            - Тип данных: title и author должны быть строками
            - Тип данных: copies_available (если указан) должен быть целым числом
            - Значение: title и author не могут быть пустыми строками
            - Значение: title и author не могут быть None
            - Значение: copies_available (если указан) не может быть отрицательным

        Args:
            title (str): Название книги для проверки
            author (str): Автор книги для проверки
            copies_available (int): Количество доступных копий книги.
                                     Может быть None, если не указано.

        Raises:
            ValueError: Если любая из проверок не пройдена.
                        Сообщение содержит подробное описание всех ошибок.
        """
        message = "Добавить книгу не удалось.\n"
        is_valid = True
        if not isinstance(title, str) or not isinstance(author, str):
            message += "Ошибка: параметры (title, author) должны быть строками.\n"
            is_valid = False
        if copies_available is not None and (not isinstance(copies_available, int) or copies_available < 0):
            message += "Ошибка: количество доступных копий книг должно быть натуральным числом.\n"
            is_valid = False
        if title == "" or author == "":
            message += "Ошибка: параметры (title, author) должны быть не пустыми строками.\n"
            is_valid = False
        if title is None or author is None:
            message += "Ошибка: параметры (title, author) должны быть не null.\n"
            is_valid = False
        if not is_valid:
            raise ValueError(message)