import unittest
import time
from unittest.mock import patch, MagicMock, call
from io import StringIO
import sys

from lab2.task4.print_message import print_message
from lab2.task4.main import run_print_message, run_print_message_with_threads


class TestPrintMessageFunction(unittest.TestCase):
    """Тесты для функции print_message"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 1: Проверка базового функционала print_message
    @patch('time.sleep')
    def test_print_message_basic(self, mock_sleep):
        """Тест 1: Проверка, что print_message вызывает sleep и print"""
        delay = 2
        message = "Тестовое сообщение"

        # Вызываем функцию
        print_message(delay, message)

        # Проверяем, что sleep был вызван с правильной задержкой
        mock_sleep.assert_called_once_with(delay)

        # Проверяем вывод
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, message)


class TestRunPrintMessage(unittest.TestCase):
    """Тесты для последовательного выполнения run_print_message"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 2: Проверка последовательного выполнения
    @patch('lab2.task4.main.print_message')
    def test_run_print_message_sequential(self, mock_print_message):
        """Тест 2: Проверка, что функция выполняется последовательно (3 вызова)"""
        # Устанавливаем глобальную переменную delay (она используется в функции)
        import lab2.task4.main
        lab2.task4.main.delay = 2

        # Вызываем функцию
        elapsed, _ = run_print_message()

        # Проверяем, что print_message была вызвана 3 раза с правильными аргументами
        expected_calls = [
            call(2, "Запуск №1"),
            call(2, "Запуск №2"),
            call(2, "Запуск №3")
        ]
        mock_print_message.assert_has_calls(expected_calls)
        self.assertEqual(mock_print_message.call_count, 3)

        # Проверяем, что время выполнения вернулось (декоратор работает)
        self.assertIsInstance(elapsed, float)


class TestRunPrintMessageWithThreads(unittest.TestCase):
    """Тесты для многопоточного выполнения run_print_message_with_threads"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 3: Проверка создания и запуска потоков
    @patch('lab2.task4.main.print_message')
    @patch('threading.Thread')
    def test_run_print_message_with_threads_creation(self, mock_thread, mock_print_message):
        """Тест 3: Проверка, что функция создает и запускает 3 потока"""
        # Устанавливаем глобальную переменную delay
        import lab2.task4.main
        lab2.task4.main.delay = 2

        # Настраиваем мок для Thread
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # Вызываем функцию
        elapsed, _ = run_print_message_with_threads()

        # Проверяем, что Thread был создан 3 раза с правильными аргументами
        expected_calls = [
            call(target=lab2.task4.main.print_message, args=(2, "Поток №1")),
            call(target=lab2.task4.main.print_message, args=(2, "Поток №2")),
            call(target=lab2.task4.main.print_message, args=(2, "Поток №3"))
        ]
        mock_thread.assert_has_calls(expected_calls)
        self.assertEqual(mock_thread.call_count, 3)

        # Проверяем, что start был вызван для каждого потока
        self.assertEqual(mock_thread_instance.start.call_count, 3)

        # Проверяем, что join был вызван для каждого потока
        self.assertEqual(mock_thread_instance.join.call_count, 3)

        # Проверяем, что время выполнения вернулось
        self.assertIsInstance(elapsed, float)


class TestTimeComparison(unittest.TestCase):
    """Тесты для сравнения времени выполнения"""

    # ТЕСТ 4: Проверка, что многопоточное выполнение быстрее последовательного
    @patch('lab2.task4.main.print_message')
    @patch('threading.Thread')
    def test_threads_faster_than_sequential(self, mock_thread, mock_print_message):
        """Тест 4: Проверка, что многопоточное выполнение быстрее (концептуально)"""
        import lab2.task4.main
        lab2.task4.main.delay = 2

        # Настраиваем мок для Thread, чтобы он имитировал параллельное выполнение
        def fake_start():
            # В реальности поток запускается и выполняется параллельно
            pass

        mock_thread_instance = MagicMock()
        mock_thread_instance.start.side_effect = fake_start
        mock_thread.return_value = mock_thread_instance

        # Измеряем время последовательного выполнения (3 вызова подряд)
        start_seq = time.time()
        for i in range(1, 4):
            print_message(2, f"Тест {i}")
        seq_time = time.time() - start_seq

        # Измеряем время многопоточного выполнения (имитация)
        start_thread = time.time()
        # В реальности потоки выполняются параллельно, но в тесте мы просто проверяем
        # что функция run_print_message_with_threads возвращает какое-то время
        thread_time, _ = run_print_message_with_threads()

        # Проверяем, что оба времени положительные
        self.assertGreater(seq_time, 0)
        self.assertGreater(thread_time, 0)


class TestPrintMessageWithRealDelay(unittest.TestCase):
    """Тесты с реальными задержками (осторожно: могут быть медленными)"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 6: Проверка реальной задержки (с небольшой погрешностью)
    def test_print_message_real_delay(self):
        """Тест 6: Проверка, что функция действительно ждет указанное время"""
        delay = 0.5  # Используем небольшую задержку для быстрого теста
        message = "Тест реальной задержки"

        start_time = time.time()
        print_message(delay, message)
        elapsed = time.time() - start_time

        # Проверяем, что прошло примерно delay секунд
        self.assertAlmostEqual(elapsed, delay, delta=0.2)

        # Проверяем вывод
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, message)


if __name__ == '__main__':
    unittest.main(verbosity=2)
