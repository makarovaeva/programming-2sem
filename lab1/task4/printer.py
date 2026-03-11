from lab1.task4.call_limiter import call_limiter


@call_limiter(limit=3)
class Printer:
    """
    Класс принтера для демонстрации работы декоратора limiter.

    Класс демонстрирует ограничение количества вызовов методов с помощью
    декоратора @limiter. Каждый метод экземпляра можно вызвать не более 3 раз.

    Attributes:
        name (str): Имя принтера
    """

    def __init__(self, name: str) -> None:
        """
        Инициализирует экземпляр принтера.

        Args:
            name (str): Имя принтера, которое будет использоваться при выводе сообщений
        """
        self.name = name

    def print_message(self, message: str) -> None:
        """
        Выводит сообщение с именем принтера.

        Args:
            message (str): Текст сообщения для вывода

        Raises:
            RuntimeError: При превышении лимита вызовов (после 3-го вызова)
        """
        print(f"[{self.name}] {message}")

    def print_greeting(self) -> None:
        """
        Выводит приветствие от имени принтера.

        Raises:
            RuntimeError: При превышении лимита вызовов (после 3-го вызова)
        """
        print(f"Привет от {self.name}!")