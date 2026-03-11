import asyncio
from lab2.task1.print_message import print_message


async def main() -> None:
    """Запускает одновременно три корутины с помощью gather"""

    await asyncio.gather(
        print_message(2, "Корутина Первая"),
        print_message(1, "Корутина Вторая"),
        print_message(3, "Корутина Третья")
    )


if __name__ == '__main__':
    """
    Точка входа в программу.
    
    Запускает корутину main для демонстрации асинхронного программирования.
    """
    asyncio.run(main())
