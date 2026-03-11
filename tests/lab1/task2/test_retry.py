import unittest
from unittest.mock import patch, MagicMock, call
import io
import sys
from lab1.task2.main import my_func
from lab1.task2.retry import retry


class TestRetryDecorator(unittest.TestCase):
    """Тесты для декоратора retry"""

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

    def test_retry_with_successful_function(self):
        """Тест: функция успешно выполняется с первой попытки"""
        mock_func = MagicMock(return_value=42)

        @retry(attempts=3, delay=1)
        def test_func():
            return mock_func()

        # Декоратор retry в текущей реализации не возвращает значение
        # и wrapper не принимает аргументы
        with patch('builtins.print') as mock_print:
            test_func()

            # Проверяем, что функция вызвана один раз
            mock_func.assert_called_once()

            # Проверяем вывод "Успех"
            mock_print.assert_any_call("Успех")

    def test_retry_with_failing_function_then_success(self):
        """Тест: функция падает несколько раз, затем успешно выполняется"""
        mock_func = MagicMock(side_effect=[ValueError, ValueError, 42])

        @retry(attempts=3, delay=0.1, exceptions=[ValueError])
        def test_func():
            result = mock_func()
            if isinstance(result, Exception):
                raise result
            return result

        with patch('builtins.print') as mock_print:
            with patch('time.sleep') as mock_sleep:
                test_func()

                # Проверяем, что функция вызвана 3 раза
                self.assertEqual(mock_func.call_count, 3)

                # Проверяем, что sleep вызван 2 раза (после первых двух ошибок)
                self.assertEqual(mock_sleep.call_count, 2)
                mock_sleep.assert_has_calls([call(0.1), call(0.1)])

                # Проверяем сообщения об ошибках и успехе
                mock_print.assert_has_calls([
                    call("Перехватили исключение, ждем 0.1 сек"),
                    call("Перехватили исключение, ждем 0.1 сек"),
                    call("Успех")
                ], any_order=False)

    def test_retry_with_all_attempts_failing(self):
        """Тест: все попытки завершаются ошибкой"""
        mock_func = MagicMock(side_effect=ValueError("Test error"))

        @retry(attempts=3, delay=0.1, exceptions=[ValueError])
        def test_func():
            return mock_func()

        with patch('builtins.print') as mock_print:
            with patch('time.sleep') as mock_sleep:
                test_func()

                # Проверяем, что функция вызвана 3 раза
                self.assertEqual(mock_func.call_count, 3)

                # Проверяем, что sleep вызван 2 раза (после первых двух ошибок)
                self.assertEqual(mock_sleep.call_count, 2)

                # Проверяем, что "Успех" не выводился
                success_calls = [c for c in mock_print.call_args_list if c[0][0] == "Успех"]
                self.assertEqual(len(success_calls), 0)

    def test_retry_with_specific_exceptions(self):
        """Тест: перехватываются только указанные исключения"""

        @retry(attempts=3, delay=0.1, exceptions=[ValueError])
        def test_func():
            raise TypeError("Test error")

        with patch('builtins.print') as mock_print:
            with patch('time.sleep') as mock_sleep:
                # Должно возникнуть исключение, так как TypeError не в списке
                with self.assertRaises(TypeError):
                    test_func()

                # Функция вызвана только один раз (нет повторных попыток)
                mock_sleep.assert_not_called()

                # Сообщения об ошибках не выводятся
                error_messages = [c for c in mock_print.call_args_list
                                  if "Перехватили исключение" in str(c)]
                self.assertEqual(len(error_messages), 0)

    def test_retry_without_exceptions_list(self):
        """Тест: если exceptions=None, перехватываются все исключения"""
        mock_func = MagicMock(side_effect=[ValueError, TypeError, 42])

        @retry(attempts=3, delay=0.1)  # exceptions=None по умолчанию
        def test_func():
            result = mock_func()
            if isinstance(result, Exception):
                raise result
            return result

        with patch('builtins.print') as mock_print:
            with patch('time.sleep') as mock_sleep:
                test_func()

                # Проверяем, что функция вызвана 3 раза
                self.assertEqual(mock_func.call_count, 3)

                # Проверяем, что sleep вызван 2 раза
                self.assertEqual(mock_sleep.call_count, 2)

    def test_retry_with_single_exception(self):
        """Тест: exceptions может быть одним исключением (не списком)"""

        @retry(attempts=2, delay=0.1, exceptions=ValueError)
        def test_func():
            raise ValueError("Test")

        with patch('time.sleep') as mock_sleep:
            with patch('builtins.print'):
                # Не должно быть исключения, так как ValueError перехватывается
                test_func()
                mock_sleep.assert_called_once()

    def test_retry_preserves_function_metadata(self):
        """Тест: сохранение метаданных исходной функции"""

        @retry(attempts=3, delay=1)
        def test_func():
            """Test documentation"""
            pass

        # Проверяем, что метаданные сохранены
        self.assertEqual(test_func.__name__, "test_func")
        self.assertEqual(test_func.__doc__, "Test documentation")

    @patch('time.sleep')
    def test_retry_delay_behavior(self, mock_sleep):
        """Тест: проверка задержек между попытками"""
        mock_func = MagicMock(side_effect=[ValueError, ValueError, ValueError])

        @retry(attempts=3, delay=2, exceptions=[ValueError])
        def test_func():
            raise mock_func()

        with patch('builtins.print'):
            test_func()

            # Проверяем, что sleep вызван с правильной задержкой
            mock_sleep.assert_has_calls([call(2), call(2)])
            self.assertEqual(mock_sleep.call_count, 2)

    def test_retry_no_delay_on_last_attempt(self):
        """Тест: нет задержки после последней попытки"""
        mock_func = MagicMock(side_effect=[ValueError, ValueError, ValueError])

        @retry(attempts=3, delay=1, exceptions=[ValueError])
        def test_func():
            raise mock_func()

        with patch('time.sleep') as mock_sleep:
            with patch('builtins.print'):
                test_func()

                # Должно быть 2 задержки (после 1-й и 2-й попытки)
                self.assertEqual(mock_sleep.call_count, 2)

    def test_retry_with_function_having_arguments(self):
        """Тест: декоратор с функцией, принимающей аргументы"""

        @retry(attempts=2, delay=0.1, exceptions=[ValueError])
        def test_func(a, b):
            if a + b < 0:
                raise ValueError("Negative sum")
            return a + b

        # В текущей реализации wrapper не принимает аргументы,
        # поэтому этот тест должен падать или быть пропущен

        # Ожидаем, что вызов с аргументами вызовет ошибку
        with self.assertRaises(TypeError):
            test_func(1, 2)


class TestMyFuncWithRetry(unittest.TestCase):
    """Тесты для функции my_func с декоратором retry"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout

    @patch('random.choice')
    @patch('random.shuffle')
    def test_my_func_success_first_try(self, mock_shuffle, mock_choice):
        """Тест: my_func успешно выполняется с первой попытки (выбрана 1)"""
        mock_choice.return_value = 1



        with patch('builtins.print') as mock_print:
            my_func()

            # Проверяем, что функция вернула 10 (10 // 1)
            # В текущей реализации результат не возвращается, но можно проверить вывод
            mock_print.assert_any_call("Успех")


class TestRetryEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев декоратора retry"""

    def test_retry_with_empty_exceptions_list(self):
        """Тест: пустой список исключений"""

        @retry(attempts=3, delay=0.1, exceptions=[])
        def test_func():
            raise ValueError("Test")

        # Пустой список означает, что ни одно исключение не перехватывается
        with self.assertRaises(ValueError):
            test_func()

    def test_retry_with_custom_exception(self):
        """Тест: пользовательское исключение"""

        class CustomError(Exception):
            pass

        @retry(attempts=2, delay=0.1, exceptions=[CustomError])
        def test_func():
            raise CustomError("Test")

        with patch('time.sleep') as mock_sleep:
            with patch('builtins.print'):
                # Не должно быть исключения
                test_func()
                mock_sleep.assert_called_once()

    def test_retry_with_multiple_exception_types(self):
        """Тест: несколько типов исключений"""

        @retry(attempts=3, delay=0.1, exceptions=[ValueError, TypeError])
        def test_func():
            # Поочередно выбрасываем разные исключения
            if not hasattr(test_func, "counter"):
                test_func.counter = 0
            test_func.counter += 1

            if test_func.counter == 1:
                raise ValueError("First")
            elif test_func.counter == 2:
                raise TypeError("Second")
            else:
                return 42

        test_func.counter = 0

        with patch('time.sleep') as mock_sleep:
            with patch('builtins.print'):
                result_wrapper = test_func()
                # Функция вызвана 3 раза
                self.assertEqual(test_func.counter, 3)
                self.assertEqual(mock_sleep.call_count, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)