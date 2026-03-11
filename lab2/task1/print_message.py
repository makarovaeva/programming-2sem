import asyncio
from lab2.time_decorator import time_decorator

@time_decorator
async def print_message(delay: int, message: str) -> None:
    """
    Функция ждет delay секунд, после чего печатает сообщение message.

    Декорирована time_decorator для измерения общего времени выполнения.
    """
    await asyncio.sleep(delay)
    print(message)