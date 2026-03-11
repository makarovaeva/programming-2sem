import threading

from lab2.task4.print_message import print_message
from lab2.time_decorator import time_decorator


@time_decorator
def run_print_message() -> None:
    """
    Запускает функцию print_message последовательно три раза в одном потоке.

    Функция используется для демонстрации последовательного выполнения задач
    без использования многопоточности. Каждый вызов print_message выполняется
    после завершения предыдущего.

    Returns:
        tuple: Кортеж из двух элементов (время выполнения, None), где первый
               элемент возвращается декоратором time_decorator
    """
    for i in range(1, 4):
        print_message(delay, f"Запуск №{i}")


@time_decorator
def run_print_message_with_threads() -> None:
    """
    Запускает функцию print_message параллельно в трех отдельных потоках.

    Функция демонстрирует использование многопоточности для параллельного
    выполнения задач. Создает три потока, каждый из которых выполняет
    print_message с уникальным номером потока. Все потоки запускаются
    одновременно, после чего главный поток ожидает их завершения.

    Returns:
        tuple: Кортеж из двух элементов (время выполнения, None), где первый
               элемент возвращается декоратором time_decorator
    """
    threads = []
    for i in range(1, 4):
        t = threading.Thread(target=print_message, args=(delay, f"Поток №{i}"))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    """
    Точка входа в программу

    Устанавливает задержку delay = 2 секунды для всех вызовов print_message.
    Сначала выполняется последовательная версия run_print_message(), затем
    параллельная версия run_print_message_with_threads(). 
    """
    delay = 2
    t, _ = run_print_message()
    print(f"Время выполнения программы с одним потоком: {t:.2f}\n")

    t, _ = run_print_message_with_threads()
    print(f"Время выполнения программы с тремя потоками: {t:.2f}")
