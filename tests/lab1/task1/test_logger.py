import unittest
import time
from unittest.mock import patch
import io
import sys
from lab1.task1.logger import logger


class TestLoggerDecorator(unittest.TestCase):
    """Тесты для декоратора logger"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout

    def get_output(self):
        """Получить захваченный вывод"""
        return self.held_output.getvalue()

    def test_logger_basic_function(self):
        """Тест логирования простой функции без аргументов"""

        @logger
        def test_func():
            return 42

        result = test_func()
        output = self.get_output()

        # Проверяем, что функция вернула правильный результат
        self.assertEqual(result, 42)

        # Проверяем наличие информации в логе
        self.assertIn("Имя функции: test_func", output)
        self.assertIn("Аргументы: позиционные=(), именованные={}", output)
        self.assertIn("Время выполнения:", output)

    def test_logger_with_positional_args(self):
        """Тест логирования функции с позиционными аргументами"""

        @logger
        def test_func(a, b):
            return a + b

        result = test_func(5, 3)
        output = self.get_output()

        self.assertEqual(result, 8)
        self.assertIn("Имя функции: test_func", output)
        self.assertIn("Аргументы: позиционные=(5, 3), именованные={}", output)

    def test_logger_with_keyword_args(self):
        """Тест логирования функции с именованными аргументами"""

        @logger
        def test_func(a, b):
            return a * b

        result = test_func(a=4, b=5)
        output = self.get_output()

        self.assertEqual(result, 20)
        self.assertIn("Аргументы: позиционные=(), именованные={'a': 4, 'b': 5}", output)

    def test_logger_with_mixed_args(self):
        """Тест логирования функции со смешанными аргументами"""

        @logger
        def test_func(a, b, c=0):
            return a + b + c

        result = test_func(1, 2, c=3)
        output = self.get_output()

        self.assertEqual(result, 6)
        self.assertIn("Аргументы: позиционные=(1, 2), именованные={'c': 3}", output)

    def test_logger_with_multiple_calls(self):
        """Тест логирования нескольких вызовов одной функции"""

        @logger
        def test_func(x):
            return x * 2

        # Первый вызов
        test_func(5)
        output1 = self.get_output()
        self.assertIn("Имя функции: test_func", output1)
        self.assertIn("Аргументы: позиционные=(5,), именованные={}", output1)

        # Очищаем вывод для второго вызова
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

        # Второй вызов
        test_func(10)
        output2 = self.get_output()
        self.assertIn("Аргументы: позиционные=(10,), именованные={}", output2)

    @patch('time.time')
    def test_logger_execution_time(self, mock_time):
        """Тест измерения времени выполнения"""
        mock_time.side_effect = [1000.0, 1001.5]  # start, end

        @logger
        def test_func():
            time.sleep(0.1)  # Имитация работы

        test_func()
        output = self.get_output()

        # Проверяем, что время выполнения было измерено
        self.assertIn("Время выполнения:", output)
        # Проверяем, что разница времени равна 1.5 секунды
        self.assertIn("1.5", output)

    def test_logger_preserves_function_metadata(self):
        """Тест сохранения метаданных исходной функции"""

        @logger
        def test_func():
            """Тестовая документация"""
            pass

        self.assertEqual(test_func.__name__, "test_func")
        self.assertEqual(test_func.__doc__, "Тестовая документация")

    def test_logger_with_function_returning_value(self):
        """Тест возврата значения из декорируемой функции"""

        @logger
        def test_func():
            return "success"

        result = test_func()
        self.assertEqual(result, "success")

    def test_logger_with_function_modifying_args(self):
        """Тест, что аргументы передаются правильно в функцию"""

        @logger
        def test_func(args_list):
            args_list.append(4)
            return args_list

        input_list = [1, 2, 3]
        result = test_func(input_list)

        self.assertEqual(result, [1, 2, 3, 4])
        self.assertEqual(input_list, [1, 2, 3, 4])  # Проверяем, что оригинальный список изменился

    def test_logger_with_default_args(self):
        """Тест функции с аргументами по умолчанию"""

        @logger
        def test_func(a, b=10):
            return a + b

        # Вызов без аргумента по умолчанию
        result1 = test_func(5)
        self.assertEqual(result1, 15)

        # Очищаем вывод
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

        # Вызов с переопределением аргумента по умолчанию
        result2 = test_func(5, b=20)
        self.assertEqual(result2, 25)

    def test_logger_handles_exceptions(self):
        """Тест обработки исключений в декорируемой функции"""

        @logger
        def test_func():
            raise ValueError("Тестовая ошибка")

        with self.assertRaises(ValueError):
            test_func()

        # Проверяем, что лог все равно был выведен
        output = self.get_output()
        self.assertIn("Имя функции: test_func", output)
        self.assertIn("Аргументы:", output)

    def test_logger_with_complex_arguments(self):
        """Тест с сложными типами аргументов"""

        @logger
        def test_func(lst, dct, st):
            return len(lst) + len(dct) + len(st)

        result = test_func([1, 2, 3], {"a": 1, "b": 2}, "test")
        output = self.get_output()

        self.assertEqual(result, 3 + 2 + 4)
        self.assertIn("Аргументы: позиционные=([1, 2, 3], {'a': 1, 'b': 2}, 'test'), именованные={}", output)

    def test_logger_with_lambda(self):
        """Тест логирования lambda-функции"""

        @logger
        def apply_lambda(func, value):
            return func(value)

        result = apply_lambda(lambda x: x * 2, 5)
        output = self.get_output()

        self.assertEqual(result, 10)
        self.assertIn("Имя функции: apply_lambda", output)

    @patch('builtins.print')
    def test_logger_calls_print(self, mock_print):
        """Тест, что декоратор вызывает print для логирования"""

        @logger
        def test_func():
            pass

        test_func()

        # Проверяем, что print был вызван 3 раза (имя, аргументы, время)
        self.assertEqual(mock_print.call_count, 3)


class TestLoggerIntegration(unittest.TestCase):
    """Интеграционные тесты для декоратора logger с примером из задания"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout


if __name__ == '__main__':
    unittest.main(verbosity=2)