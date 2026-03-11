from lab1.task3.logger import logger


@logger(show_magic_methods=False, show_result=True)
class Calculator:
    """
    Калькулятор для выполнения базовых арифметических операций.

    Класс демонстрирует работу декоратора logger, который логирует
    вызовы всех методов (кроме магических, так как show_magic_methods=False).

    Attributes:
        name (str): Название калькулятора
    """

    def __init__(self, name: str):
        """
        Инициализирует экземпляр калькулятора.

        Args:
            name (str): Название калькулятора
        """
        self.name = name

    def add(self, a: float, b: float) -> float:
        """
        Сложение двух чисел.

        Args:
            a (float): Первое слагаемое
            b (float): Второе слагаемое

        Returns:
            float: Сумма a и b
        """
        return a + b

    def divide(self, a: float, b: float) -> float | ValueError:
        """
        Деление с проверкой на ноль.

        Args:
            a (float): Делимое
            b (float): Делитель

        Returns:
            float: Результат деления a на b

        Raises:
            ValueError: Если b равно 0 (деление на ноль)
        """
        if b == 0:
            raise ValueError("Деление на ноль!")
        return a / b

    def __str__(self) -> str:
        """
        Возвращает строковое представление калькулятора.

        Returns:
            str: Строка вида "Калькулятор: {name}"
        """
        return f"Калькулятор: {self.name}"

    def __len__(self) -> int:
        """
        Возвращает длину названия калькулятора.

        Returns:
            int: Количество символов в названии калькулятора
        """
        return len(self.name)