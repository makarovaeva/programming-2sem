import unittest
import asyncio
import time
from unittest.mock import patch, call
from io import StringIO
import sys

from lab2.task1.print_message import print_message
from lab2.task2.main import main


class TestMainAsyncGather(unittest.IsolatedAsyncioTestCase):
    """Тесты для асинхронной функции main с asyncio.gather"""

    async def asyncSetUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    async def asyncTearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 1: Проверка, что все три сообщения выводятся
    async def test_all_messages_printed(self):
        """Тест 1: Проверка, что функция выводит все три сообщения"""
        await main()

        output = self.held_output.getvalue()

        # Проверяем наличие всех трех сообщений
        self.assertIn("Корутина Первая", output)
        self.assertIn("Корутина Вторая", output)
        self.assertIn("Корутина Третья", output)

        # Проверяем, что сообщений ровно 3 (каждое с новой строки)
        lines = output.strip().split('\n')
        self.assertEqual(len(lines), 3)

    # ТЕСТ 2: Проверка времени выполнения (конкурентность)
    async def test_concurrent_execution_time(self):
        """Тест 2: Проверка, что функции выполняются конкурентно (общее время ~3 сек)"""
        start_time = time.time()
        await main()
        elapsed = time.time() - start_time

        # При последовательном выполнении было бы 2+1+3 = 6 секунд
        # При конкурентном - максимум 3 секунды (самая долгая)
        self.assertLess(elapsed, 3.5)  # Даем небольшую погрешность
        self.assertGreater(elapsed, 2.5)  # Должно быть около 3 секунд

    # ТЕСТ 3: Проверка порядка вывода с помощью моков
    @patch('lab2.task2.main.print_message')
    async def test_gather_calls_all_functions(self, mock_print_message):
        """Тест 3: Проверка, что gather вызывает все три функции"""
        # Настраиваем мок
        mock_print_message.return_value = None

        # Вызываем main
        await main()

        # Проверяем, что print_message была вызвана 3 раза с правильными аргументами
        expected_calls = [
            call(2, "Корутина Первая"),
            call(1, "Корутина Вторая"),
            call(3, "Корутина Третья")
        ]
        mock_print_message.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_print_message.call_count, 3)


class TestAsyncGatherBehavior(unittest.TestCase):
    """Тесты для поведения asyncio.gather"""

    # ТЕСТ 5: Проверка обработки исключений
    def test_exception_propagation(self):
        """Тест 5: Проверка, что исключения пробрасываются корректно"""

        async def failing_coroutine():
            raise ValueError("Тестовая ошибка")

        async def run_gather():
            await asyncio.gather(
                print_message(1, "Нормальная"),
                failing_coroutine(),
                print_message(2, "Еще одна")
            )

        # Проверяем, что исключение пробрасывается
        with self.assertRaises(ValueError) as context:
            asyncio.run(run_gather())

        self.assertEqual(str(context.exception), "Тестовая ошибка")


if __name__ == '__main__':
    unittest.main(verbosity=2)
