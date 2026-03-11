import time


def print_message(delay: int, message: str) -> None:
    """Функция ждет delay секунд, после чего печатает сообщение message"""

    time.sleep(delay)
    print(message)
