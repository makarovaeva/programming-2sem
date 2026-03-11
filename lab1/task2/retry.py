import time
from functools import wraps


def retry(attempts: int, delay: int, exceptions: list[type[Exception]] = None) -> callable:
    """
    Декоратор для повторного выполнения функции при возникновении исключений.

    Позволяет автоматически повторять вызов функции указанное количество раз
    при возникновении определенных типов исключений.

    Args:
        attempts (int): Максимальное количество попыток выполнения функции
        delay (int): Задержка в секундах между попытками
        exceptions (list[type[Exception]], optional): Список типов исключений,
            при которых следует повторять попытку. Если None (по умолчанию),
            перехватываются все исключения.

    Returns:
        callable: Декоратор, который оборачивает функцию логикой повторных попыток
    """

    def decorator(func: callable) -> callable:
        """
        Внутренний декоратор, принимающий функцию для обертывания.

        Args:
            func (callable): Декорируемая функция

        Returns:
            callable: Функция-обертка с логикой повторных попыток
        """
        @wraps(func)
        def wrapper() -> None:
            """
            Функция-обертка, реализующая логику повторных попыток.

            Последовательно выполняет декорируемую функцию до attempts раз,
            пока не будет достигнут успех или не исчерпаны все попытки.

            Returns:
                None: Функция ничего не возвращает
            """
            if exceptions is not None:
                if isinstance(exceptions, list):
                    exception_types = tuple(exceptions)
                else:
                    exception_types = (exceptions,)
            else:
                exception_types = Exception
            for i in range(attempts):
                flag = True
                try:
                    func()
                except exception_types:
                    flag = False
                    if i == (attempts - 1): break
                    print(f"Перехватили исключение, ждем {delay} сек")
                    time.sleep(delay)
                if flag:
                    print("Успех")
                    break

        return wrapper

    return decorator