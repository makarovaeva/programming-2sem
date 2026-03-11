import asyncio
from lab2.task1.print_message import print_message

if __name__ == '__main__':
    """
    Точка входа в программу
    
    Вызывает функцию print_message в асинхронном режиме
    с задержкой в delay секунд и сообщением 'Спустя {delay} сек'.
    Выводит время выполнения функции для измерения и проверки задержки.    
    """

    delay = 5
    t, _ = asyncio.run(print_message(delay, f"Спустя {delay} сек"))
    print(f"Время, измеренное декоратором: {t:.2f} сек")
