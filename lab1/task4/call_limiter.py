import functools
from collections import defaultdict
from typing import Callable, Dict, Any


def call_limiter(limit: int) -> Callable:
    """
    Декоратор для ограничения количества вызовов методов класса.

    Args:
        limit: максимальное количество вызовов для каждого метода

    Raises:
        ValueError: если limit меньше 1

    Returns:
        Callable: Декоратор класса, который оборачивает методы логикой ограничения вызовов
    """
    if limit < 1:
        raise ValueError("Лимит вызовов должен быть больше 0")

    def class_decorator(cls: callable) -> type:
        """
        Внутренний декоратор, принимающий класс для обертывания.

        Args:
            cls: Декорируемый класс

        Returns:
            type: Тот же класс, но с обернутыми методами и добавленными служебными методами
        """

        # Словарь для хранения счетчиков вызовов для каждого метода каждого экземпляра
        # Формат: {id(instance): {method_name: counter}}
        call_counters: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        def method_decorator(method: Callable) -> Callable:
            """
            Декоратор для отдельного метода класса.

            Args:
                method (Callable): Оригинальный метод класса

            Returns:
                Callable: Обернутый метод с проверкой лимита вызовов
            """

            @functools.wraps(method)
            def wrapper(self, *args, **kwargs) -> Any:
                """
                Функция-обертка для выполнения метода с проверкой лимита вызовов.

                Args:
                    self: Ссылка на экземпляр класса
                    *args: Позиционные аргументы метода
                    **kwargs: Именованные аргументы метода

                Returns:
                    Any: Результат выполнения оригинального метода

                Raises:
                    RuntimeError: Если превышен лимит вызовов для данного метода
                """
                instance_id = id(self)
                method_name = method.__name__

                # Проверяем текущее количество вызовов
                current_calls = call_counters[instance_id][method_name]

                if current_calls >= limit:
                    raise RuntimeError(
                        f"Метод '{method_name}' превысил лимит вызовов ({limit}). "
                        f"Попытка вызова #{current_calls + 1}"
                    )

                # Увеличиваем счетчик
                call_counters[instance_id][method_name] += 1

                # Выполняем метод
                return method(self, *args, **kwargs)

            return wrapper

        # Оборачиваем все методы класса
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                setattr(cls, attr_name, method_decorator(attr_value))

        return cls

    return class_decorator