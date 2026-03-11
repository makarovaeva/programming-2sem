import asyncio
import time

from lab1.task5.first_func import first_function
from lab1.task5.second_func import second_function


async def run_concurrently():
    """Запуск функций конкурентно (одновременно) с помощью gather"""

    start_time = time.time()

    # Функции выполняются одновременно
    results = await asyncio.gather(
        first_function("Конкурентная 1"),
        second_function("Конкурентная 2")
    )

    end_time = time.time()
    print(f"\nРезультаты: {results[0]}, {results[1]}")
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")