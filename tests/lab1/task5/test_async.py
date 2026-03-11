import unittest
import io
import sys
from unittest.mock import patch, AsyncMock
from datetime import datetime
from lab1.task5.current_time import current_time
from lab1.task5.first_func import first_function
from lab1.task5.second_func import second_function
from lab1.task5.run_concurrently import run_concurrently


class TestCurrentTime(unittest.TestCase):
    """Тесты для функции current_time"""

    @patch('lab1.task5.current_time.datetime')
    def test_current_time_format(self, mock_datetime):
        """Тест 1: Проверка формата возвращаемого времени"""

        # Создаем фиксированное время для теста
        fixed_time = datetime(2024, 3, 15, 14, 30, 45, 123456)
        mock_datetime.now.return_value = fixed_time

        result = current_time()

        # Проверяем формат (ЧЧ:ММ:СС.ммм)
        self.assertEqual(result, "14:30:45.123")
        self.assertEqual(len(result), 12)  # Длина строки "14:30:45.123"

        # Проверяем, что обрезаны только микросекунды до миллисекунд
        mock_datetime.now.assert_called_once()

    @patch('lab1.task5.current_time.datetime')
    def test_current_time_edge_cases(self, mock_datetime):
        """Тест 2: Проверка граничных значений времени"""

        # Тест с разными значениями миллисекунд
        test_cases = [
            (datetime(2024, 1, 1, 0, 0, 0, 0), "00:00:00.000"),
            (datetime(2024, 1, 1, 23, 59, 59, 999000), "23:59:59.999"),
            (datetime(2024, 1, 1, 9, 5, 3, 7000), "09:05:03.007"),  # 7000 микросекунд = 7 мс
        ]

        for mock_time, expected in test_cases:
            mock_datetime.now.return_value = mock_time
            result = current_time()
            self.assertEqual(result, expected)


class TestAsyncFunctions(unittest.IsolatedAsyncioTestCase):
    """Тесты для асинхронных функций"""

    async def asyncSetUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    async def asyncTearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    @patch('lab1.task5.first_func.current_time')
    async def test_first_function_execution(self, mock_current_time):
        """Тест 3: Проверка выполнения первой функции"""

        # Мокаем время для предсказуемого вывода
        mock_current_time.side_effect = [
            "00:00:00.000", "00:00:00.000", "00:00:01.000",
            "00:00:05.000", "00:00:05.000"
        ]

        # Мокаем asyncio.sleep для ускорения теста
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            result = await first_function("Тестовая 1")

            # Проверяем возвращаемое значение
            self.assertEqual(result, "Тестовая 1 завершена")

            # Проверяем, что sleep вызывался с правильными задержками
            mock_sleep.assert_has_awaits([
                unittest.mock.call(1),
                unittest.mock.call(4)
            ])

            # Получаем вывод
            output = self.held_output.getvalue()

            # Проверяем последовательность вывода
            expected_outputs = [
                "[00:00:00.000] Тестовая 1: Начало выполнения",
                "[00:00:00.000] Тестовая 1: Принт 1",
                "[00:00:01.000] Тестовая 1: Принт 2",
                "[00:00:05.000] Тестовая 1: Принт 3",
                "[00:00:05.000] Тестовая 1: Завершение выполнения"
            ]

            for expected in expected_outputs:
                self.assertIn(expected, output)

    @patch('lab1.task5.second_func.current_time')
    async def test_second_function_execution(self, mock_current_time):
        """Тест 4: Проверка выполнения второй функции"""

        # Мокаем время для предсказуемого вывода
        mock_current_time.side_effect = [
            "00:00:00.000", "00:00:00.000", "00:00:03.000",
            "00:00:04.000", "00:00:05.000", "00:00:05.000"
        ]

        # Мокаем asyncio.sleep для ускорения теста
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            result = await second_function("Тестовая 2")

            # Проверяем возвращаемое значение
            self.assertEqual(result, "Тестовая 2 завершена")

            # Проверяем, что sleep вызывался с правильными задержками
            mock_sleep.assert_has_awaits([
                unittest.mock.call(3),
                unittest.mock.call(1),
                unittest.mock.call(1)
            ])

            # Получаем вывод
            output = self.held_output.getvalue()

            # Проверяем последовательность вывода
            expected_outputs = [
                "[00:00:00.000] Тестовая 2: Начало выполнения",
                "[00:00:00.000] Тестовая 2: Принт 1",
                "[00:00:03.000] Тестовая 2: Принт 2",
                "[00:00:04.000] Тестовая 2: Принт 3",
                "[00:00:05.000] Тестовая 2: Принт 4",
                "[00:00:05.000] Тестовая 2: Завершение выполнения"
            ]

            for expected in expected_outputs:
                self.assertIn(expected, output)

    @patch('lab1.task5.run_concurrently.first_function')
    @patch('lab1.task5.run_concurrently.second_function')
    @patch('lab1.task5.run_concurrently.time')
    async def test_run_concurrently(self, mock_time, mock_second, mock_first):
        """Тест 5: Проверка конкурентного выполнения"""

        # Настраиваем моки для времени
        mock_time.time.side_effect = [1000.0, 1005.0]  # start, end

        # Настраиваем моки для функций
        mock_first.return_value = "Конкурентная 1 завершена"
        mock_second.return_value = "Конкурентная 2 завершена"

        # Захватываем вывод
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            await run_concurrently()

            output = fake_output.getvalue()

            # Проверяем вызовы функций
            mock_first.assert_called_once_with("Конкурентная 1")
            mock_second.assert_called_once_with("Конкурентная 2")

            # Проверяем вывод результатов
            self.assertIn("Результаты: Конкурентная 1 завершена, Конкурентная 2 завершена", output)
            self.assertIn("Общее время выполнения: 5.00 секунд", output)


if __name__ == '__main__':
    unittest.main(verbosity=2)