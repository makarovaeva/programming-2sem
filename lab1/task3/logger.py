import time
import functools
from datetime import datetime
from typing import Callable


def logger(show_magic_methods: bool = False, show_result: bool = False) -> Callable:
    """
    Декоратор для логирования всех методов класса.

    Args:
        show_magic_methods: если True, логировать также магические методы
        show_result: если True, выводить также результат выполнения метода

    Returns:
        Callable: Декоратор класса, который оборачивает класс в LoggerWrapper
    """

    def class_decorator(cls: callable) -> Callable:
        """
        Внутренний декоратор, принимающий класс для обертывания.

        Args:
            cls: Декорируемый класс

        Returns:
            LoggerWrapper: Обертка класса с логированием методов
        """

        class LoggerWrapper:
            """
            Класс-обертка для логирования вызовов методов оригинального класса.

            Перехватывает все обращения к атрибутам и методам экземпляра,
            добавляя логирование для вызываемых методов.
            """

            def __init__(self, *args, **kwargs) -> None:
                """
                Инициализирует обертку, создавая экземпляр оригинального класса.

                Args:
                    *args: Позиционные аргументы для конструктора оригинального класса
                    **kwargs: Именованные аргументы для конструктора оригинального класса
                """
                self.instance = cls(*args, **kwargs)

            def __getattr__(self, name: str) -> Callable[[Callable], str] | str:
                """
                Перехватывает обращение к атрибутам экземпляра.

                Если запрашиваемый атрибут является вызываемым (методом),
                оборачивает его в логирующую функцию.

                Args:
                    name (str): Имя запрашиваемого атрибута

                Returns:
                    Any: Значение атрибута или обернутый метод
                """
                attr = getattr(self.instance, name)
                if callable(attr):
                    return self._log_method_call(attr, name)
                return attr

            def _log_method_call(self, method: Callable, method_name: str) -> Callable:
                """
                Создает обертку для метода с логированием.

                Args:
                    method (Callable): Оригинальный метод
                    method_name (str): Имя метода

                Returns:
                    Callable: Обернутый метод с логированием
                """

                @functools.wraps(method)
                def wrapper(*args, **kwargs):
                    """
                    Функция-обертка для выполнения метода с логированием.

                    Args:
                        *args: Позиционные аргументы метода
                        **kwargs: Именованные аргументы метода

                    Returns:
                        Any: Результат выполнения оригинального метода

                    Raises:
                        Exception: Пробрасывает исключения оригинального метода
                                  после их логирования
                    """
                    # Проверяем, нужно ли логировать магический метод
                    if not show_magic_methods and method_name.startswith('__') and method_name.endswith('__'):
                        return method(*args, **kwargs)

                    class_name = self.instance.__class__.__name__

                    start_time = time.time()
                    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                    try:
                        result = method(*args, **kwargs)

                        execution_time = (time.time() - start_time) * 1000  # в миллисекундах

                        # Формируем строку логирования
                        log_parts = [
                            f"[{start_datetime}]",
                            f"Класс: {class_name}",
                            f"Метод: {method_name}",
                            f"Аргументы: позиционные={args}, именованные={kwargs}",
                            f"Время: {execution_time:.3f}мс"
                        ]

                        if show_result:
                            log_parts.append(f"Результат: {result}")

                        print(" | ".join(log_parts))

                        return result

                    except Exception as e:
                        # Логируем ошибку, если она произошла
                        execution_time = (time.time() - start_time) * 1000
                        print(f"[{start_datetime}] | Класс: {class_name} | Метод: {method_name} | "
                              f"ОШИБКА: {type(e).__name__}: {e} | Время: {execution_time:.3f}мс")
                        raise

                return wrapper

        return LoggerWrapper

    return class_decorator