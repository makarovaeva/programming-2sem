import unittest
import asyncio
import time
from unittest.mock import patch, AsyncMock
from io import StringIO
import sys
from lab2.task1.print_message import print_message


class TestPrintMessage(unittest.IsolatedAsyncioTestCase):
    """Тесты для асинхронной функции print_message"""

    async def asyncSetUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    async def asyncTearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 1: Проверка базового функционала
    async def test_print_message_basic_functionality(self):
        """Тест 1: Проверка, что функция ожидает заданное время и выводит сообщение"""
        delay = 1
        message = "Тестовое сообщение"

        start_time = time.time()
        elapsed, result = await print_message(delay, message)
        end_time = time.time()

        # Проверяем, что прошло примерно delay секунд
        actual_delay = end_time - start_time
        self.assertAlmostEqual(actual_delay, delay, delta=0.2)

        # Проверяем возвращаемое значение декоратора
        self.assertIsNone(result)
        self.assertIsInstance(elapsed, float)
        self.assertGreaterEqual(elapsed, delay)

        # Проверяем вывод
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, message)

    # ТЕСТ 2: Проверка с разными задержками
    async def test_print_message_with_different_delays(self):
        """Тест 2: Проверка работы функции с разными значениями задержки"""
        test_cases = [
            (0.1, "Быстрое сообщение"),
            (0.5, "Среднее сообщение"),
            (1.0, "Длинное сообщение")
        ]

        for delay, message in test_cases:
            # Очищаем вывод для каждого случая
            self.held_output.truncate(0)
            self.held_output.seek(0)

            start_time = time.time()
            elapsed, result = await print_message(delay, message)
            end_time = time.time()

            # Проверяем время выполнения
            actual_delay = end_time - start_time
            self.assertAlmostEqual(actual_delay, delay, delta=0.2)
            self.assertAlmostEqual(elapsed, delay, delta=0.2)
            self.assertIsNone(result)

            # Проверяем вывод
            output = self.held_output.getvalue().strip()
            self.assertEqual(output, message)

    # ТЕСТ 3: Проверка с пустым сообщением
    async def test_print_message_with_empty_message(self):
        """Тест 3: Проверка работы функции с пустой строкой в качестве сообщения"""
        delay = 0.3
        message = ""

        elapsed, result = await print_message(delay, message)

        # Проверяем время
        self.assertAlmostEqual(elapsed, delay, delta=0.2)
        self.assertIsNone(result)

        # Проверяем вывод (пустая строка)
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, message)

    # ТЕСТ 4: Проверка с нулевой задержкой
    async def test_print_message_with_zero_delay(self):
        """Тест 4: Проверка работы функции с нулевой задержкой"""
        delay = 0
        message = "Мгновенное сообщение"

        elapsed, result = await print_message(delay, message)

        # Проверяем, что время близко к нулю
        self.assertLess(elapsed, 0.01)
        self.assertIsNone(result)

        # Проверяем вывод
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, message)


class TestPrintMessageWithMocks(unittest.TestCase):
    """Тесты с использованием моков для изоляции"""

    # ТЕСТ 6: Проверка вызова asyncio.sleep
    @patch('asyncio.sleep', new_callable=AsyncMock)
    def test_asyncio_sleep_called(self, mock_sleep):
        """Тест 6: Проверка, что функция вызывает asyncio.sleep с правильным аргументом"""
        delay = 2
        message = "Тест"

        async def run_test():
            elapsed, result = await print_message(delay, message)
            return elapsed, result

        # Запускаем тест
        elapsed, result = asyncio.run(run_test())

        # Проверяем, что sleep был вызван с правильной задержкой
        mock_sleep.assert_called_once_with(delay)

        # Проверяем результат
        self.assertIsNone(result)
        self.assertIsInstance(elapsed, float)

    # ТЕСТ 8: Проверка обработки исключений
    @patch('asyncio.sleep', side_effect=Exception("Тестовая ошибка"))
    def test_exception_handling(self, mock_sleep):
        """Тест 8: Проверка, что исключения пробрасываются корректно"""
        delay = 1
        message = "Тест"

        async def run_test():
            with self.assertRaises(Exception) as context:
                await print_message(delay, message)
            return str(context.exception)

        error_message = asyncio.run(run_test())
        self.assertEqual(error_message, "Тестовая ошибка")


class TestTimeDecoratorIntegration(unittest.TestCase):
    """Тесты для проверки интеграции с time_decorator"""

    # ТЕСТ 9: Проверка возвращаемого значения декоратора
    def test_decorator_return_value_structure(self):
        """Тест 9: Проверка структуры возвращаемого значения декоратора"""
        delay = 0.2
        message = "Интеграционный тест"

        async def run_test():
            result = await print_message(delay, message)
            return result

        # Запускаем функцию и проверяем структуру возврата
        elapsed, func_result = asyncio.run(run_test())

        # Проверяем, что возвращается кортеж из двух элементов
        self.assertIsInstance(elapsed, float)
        self.assertIsNone(func_result)

    # ТЕСТ 10: Проверка точности измерения времени
    @patch('time.time')
    def test_time_measurement_accuracy(self, mock_time):
        """Тест 10: Проверка точности измерения времени декоратором"""
        # Настраиваем мок для time.time
        mock_time.side_effect = [1000.0, 1002.5]  # start, end

        delay = 2.5
        message = "Тест времени"

        async def run_test():
            elapsed, result = await print_message(delay, message)
            return elapsed, result

        # Запускаем с подменой asyncio.sleep
        with patch('asyncio.sleep', new_callable=AsyncMock):
            elapsed, result = asyncio.run(run_test())

        # Проверяем, что время вычислено правильно (1002.5 - 1000.0 = 2.5)
        self.assertEqual(elapsed, 2.5)
        self.assertIsNone(result)


class TestPrintMessageEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев"""

    # ТЕСТ 11: Проверка с очень длинным сообщением
    def test_print_message_with_very_long_message(self):
        """Тест 11: Проверка работы с очень длинным сообщением"""
        delay = 0.1
        message = "A" * 10000  # Строка из 10000 символов

        async def run_test():
            elapsed, result = await print_message(delay, message)
            return elapsed, result

        # Захватываем вывод
        with patch('sys.stdout', new=StringIO()) as fake_output:
            elapsed, result = asyncio.run(run_test())
            output = fake_output.getvalue().strip()

        # Проверяем, что сообщение выведено полностью
        self.assertEqual(output, message)
        self.assertIsNone(result)
        self.assertAlmostEqual(elapsed, delay, delta=0.2)

    # ТЕСТ 12: Проверка с многобайтовыми символами
    def test_print_message_with_unicode(self):
        """Тест 12: Проверка работы с Unicode символами"""
        delay = 0.1
        message = "Привет, мир!"

        async def run_test():
            elapsed, result = await print_message(delay, message)
            return elapsed, result

        with patch('sys.stdout', new=StringIO()) as fake_output:
            elapsed, result = asyncio.run(run_test())
            output = fake_output.getvalue().strip()

        # Проверяем, что Unicode символы корректно обрабатываются
        self.assertEqual(output, message)
        self.assertIsNone(result)
        self.assertAlmostEqual(elapsed, delay, delta=0.2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
