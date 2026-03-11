import asyncio
from lab1.task5.current_time import current_time


async def first_function(name: str = "Функция 1"):
    """
    Первая асинхронная функция:
    - Принт 1
    - asyncio.sleep(1)
    - Принт 2
    - asyncio.sleep(4)
    - Принт 3
    """
    print(f"[{current_time()}] {name}: Начало выполнения")

    print(f"[{current_time()}] {name}: Принт 1")
    await asyncio.sleep(1)

    print(f"[{current_time()}] {name}: Принт 2")
    await asyncio.sleep(4)

    print(f"[{current_time()}] {name}: Принт 3")

    print(f"[{current_time()}] {name}: Завершение выполнения")
    return f"{name} завершена"