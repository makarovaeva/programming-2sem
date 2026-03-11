import time

from lab1.task5.first_func import first_function
from lab1.task5.second_func import second_function


async def run_sequentially():
    """Запуск функций последовательно (одна за другой)"""

    start_time = time.time()

    # Функции выполняются одна за другой
    result1 = await first_function("Последовательная 1")
    result2 = await second_function("Последовательная 2")

    end_time = time.time()
    print(f"\nРезультаты: {result1}, {result2}")
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")