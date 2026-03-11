import asyncio

from lab2.task3.http_client import HttpClient

if __name__ == '__main__':
    """
    Точка входа в программу
    
    Создает список urls из переданных url сайтов, создает экземпляр класса HttpClient,
    после чего выполняет синхронные и асинхронные запросы к сайтам
    для демонстрации преимущества в эффективности у асинхронного подхода
    """

    path1 = "https://app.weeek.net/"
    path2 = "https://google.com/"
    path3 = "https://vk.com/"
    urls = [path1, path2, path3]
    http_client = HttpClient(urls)

    print("Делаем запросы синхронно:")
    t = http_client.print_sync_responses()
    print(f"Общее время работы составило {t:.2f} сек")

    print("\nДелаем запросы асинхронно:")
    t = asyncio.run(http_client.print_async_responses())
    print(f"Общее время работы составило {t:.2f} сек")
