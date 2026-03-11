import threading
import time


def increment_with_lock(lock: threading.Lock) -> None:
    """Функция, увеличивающая счетчик с использованием блокировки"""

    global counter
    for _ in range(iterations):
        with lock:  # Синхронизация доступа
            current = counter
            time.sleep(0.00000001)
            counter = current + 1


def solution_race_condition() -> None:
    """Демонстрация решения гонки данных"""

    lock = threading.Lock()
    threads = []
    for i in range(5):
        t = threading.Thread(target=increment_with_lock, args=(lock,), name=f"Поток {i}")
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
    Запускает скрипт для демонстрации решения проблемы гонки данных
    """
    counter = 0
    iterations = 100
    solution_race_condition()
