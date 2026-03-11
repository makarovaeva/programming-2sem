import asyncio

from lab1.task5.run_concurrently import run_concurrently
from lab1.task5.run_sequentially import run_sequentially

if __name__ == '__main__':
    """
    Скрипт для сравнения последовательного и конкурентного выполнения асинхронных функций.

    Этот скрипт импортирует две функции из модулей task5:
    - run_concurrently() - запускает две асинхронные функции одновременно (конкурентно)
    - run_sequentially() - запускает две асинхронные функции последовательно

    И выполняет их с помощью asyncio.run() для демонстрации разницы в времени выполнения.
    """

    print("Функции выполняются одновременно:")
    asyncio.run(run_concurrently())

    print("Функции выполняются последовательно")
    asyncio.run(run_sequentially())