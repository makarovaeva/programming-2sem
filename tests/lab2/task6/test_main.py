import unittest
import threading

from unittest.mock import  MagicMock

from lab2.task6.main import increment_with_lock, solution_race_condition


class TestRaceConditionSolution(unittest.TestCase):
    """Простые тесты для функций из задания 6 (решение гонки данных)"""

    def setUp(self):
        """Сброс глобальных переменных перед каждым тестом"""
        import lab2.task6.main
        lab2.task6.main.counter = 0
        lab2.task6.main.iterations = 10
        self.module = lab2.task6.main

    # ТЕСТ 1: Проверка, что increment_with_lock увеличивает счетчик
    def test_increment_increases_counter(self):
        """Тест 1: Функция должна увеличивать глобальный счетчик"""
        self.module.counter = 5
        self.module.iterations = 3
        lock = threading.Lock()

        increment_with_lock(lock)

        self.assertEqual(self.module.counter, 8)

    # ТЕСТ 2: Проверка, что функция вызывается нужное количество раз
    def test_increment_called_correct_number_of_times(self):
        """Тест 2: Функция должна выполнять iterations итераций"""
        self.module.counter = 0
        self.module.iterations = 7
        lock = threading.Lock()

        increment_with_lock(lock)

        self.assertEqual(self.module.counter, 7)

    # ТЕСТ 3: Проверка, что функция использует блокировку
    def test_increment_uses_lock(self):
        """Тест 3: Функция должна использовать переданную блокировку"""
        self.module.counter = 0
        self.module.iterations = 1

        # Создаем мок для блокировки
        mock_lock = MagicMock()

        increment_with_lock(mock_lock)

        # Проверяем, что блокировка использовалась
        mock_lock.__enter__.assert_called_once()
        mock_lock.__exit__.assert_called_once()

    # ТЕСТ 5: Проверка, что решение дает правильный результат
    def test_solution_gives_correct_result(self):
        """Тест 5: При использовании блокировки счетчик должен быть правильным"""
        self.module.counter = 0
        self.module.iterations = 100

        # Запускаем решение
        solution_race_condition()

        # Проверяем, что значение правильное (нет гонки данных)
        self.assertEqual(self.module.counter, 500)  # 5 потоков * 100 итераций


if __name__ == '__main__':
    unittest.main()
