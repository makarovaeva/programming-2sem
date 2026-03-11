import threading
import time


def increment_without_lock() -> None:
    """Функция, увеличивающая счетчик без синхронизации"""

    global counter
    for _ in range(iterations):
        current = counter
        time.sleep(0.00000001)
        counter = current + 1


def demonstrate_race_condition() -> None:
    """Демонстрация проблемы гонки данных"""

    threads = []
    for i in range(5):
        t = threading.Thread(target=increment_without_lock, name=f"Поток {i}")
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    expected = 5 * iterations
    print(f"Ожидаемое значение: {expected}")
    print(f"Фактическое значение: {counter}")


if __name__ == "__main__":
    """
    Точка входа в программу

    Создает глобальные переменные    
    Запускает скрипт для демонстрации проблемы гонки данных
    """
    counter = 0
    iterations = 100
    demonstrate_race_condition()
