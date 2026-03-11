import asyncio
from lab1.task5.current_time import current_time


async def second_function(name: str = "Функция 2"):
    """
    Вторая асинхронная функция:
    - Принт 1
    - asyncio.sleep(3)
    - Принт 2
    - asyncio.sleep(1)
    - Принт 3
    - asyncio.sleep(1)
    - Принт 4
    """
    print(f"[{current_time()}] {name}: Начало выполнения")

    print(f"[{current_time()}] {name}: Принт 1")
    await asyncio.sleep(3)

    print(f"[{current_time()}] {name}: Принт 2")
    await asyncio.sleep(1)

    print(f"[{current_time()}] {name}: Принт 3")
    await asyncio.sleep(1)

    print(f"[{current_time()}] {name}: Принт 4")

    print(f"[{current_time()}] {name}: Завершение выполнения")
    return f"{name} завершена"