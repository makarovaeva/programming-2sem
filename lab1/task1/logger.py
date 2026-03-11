import time
from typing import Any, Callable
from functools import wraps


def logger(func: callable) -> Callable:
    """
    Декоратор для логирования вызова функции.

    Выводит информацию о:
    - имени вызываемой функции
    - переданных аргументах (позиционных и именованных)
    - времени выполнения функции

    Args:
        func (callable): Декорируемая функция

    Returns:
        Callable: Функция-обёртка, которая добавляет логирование
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """
        Функция-обёртка, которая выполняет декорируемую функцию с логированием.

        Args:
            *args: Позиционные аргументы для декорируемой функции
            **kwargs: Именованные аргументы для декорируемой функции

        Returns:
            Any: Функция возвращает то, что возвращает переданная функция
        """
        print(f"Имя функции: {wrapper.__name__}")
        print(f"Аргументы: позиционные={args}, именованные={kwargs}")
        start = time.time()
        res = func(*args, **kwargs)
        print(f"Время выполнения: {time.time() - start}")
        return res

    return wrapper