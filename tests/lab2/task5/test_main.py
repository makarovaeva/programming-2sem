import unittest

from lab2.task5.main import increment_without_lock


class TestRaceCondition(unittest.TestCase):
    """Простые тесты для функций из задания 5"""

    def setUp(self):
        """Сброс глобальных переменных перед каждым тестом"""
        import lab2.task5.main
        lab2.task5.main.counter = 0
        lab2.task5.main.iterations = 10
        self.module = lab2.task5.main

    # ТЕСТ 1: Проверка, что increment_without_lock увеличивает счетчик
    def test_increment_increases_counter(self):
        """Тест 1: Функция должна увеличивать глобальный счетчик"""
        self.module.counter = 5
        self.module.iterations = 3

        increment_without_lock()

        self.assertEqual(self.module.counter, 8)

    # ТЕСТ 2: Проверка, что функция вызывается нужное количество раз
    def test_increment_called_correct_number_of_times(self):
        """Тест 2: Функция должна выполнять iterations итераций"""
        self.module.counter = 0
        self.module.iterations = 7

        increment_without_lock()

        self.assertEqual(self.module.counter, 7)


if __name__ == '__main__':
    unittest.main()
