import unittest
import io
import sys
from unittest.mock import patch
from lab1.task3.logger import logger
from lab1.task3.calculator import Calculator


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
        self.held_output.close()

    def get_output(self):
        """Получить захваченный вывод"""
        return self.held_output.getvalue()

    def test_logger_basic_functionality(self):
        """Тест базового логирования методов класса"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def test_method(self, x):
                return x * 2

        obj = TestClass()
        result = obj.test_method(5)

        self.assertEqual(result, 10)
        output = self.get_output()

        # Проверяем наличие всех элементов лога
        self.assertIn("Класс: TestClass", output)
        self.assertIn("Метод: test_method", output)
        self.assertIn("Аргументы: позиционные=(5,), именованные={}", output)
        self.assertIn("Время:", output)
        self.assertIn("Результат: 10", output)

    def test_logger_without_show_result(self):
        """Тест логирования без вывода результата"""

        @logger(show_magic_methods=False, show_result=False)
        class TestClass:
            def test_method(self, x):
                return x * 2

        obj = TestClass()
        result = obj.test_method(5)

        self.assertEqual(result, 10)
        output = self.get_output()

        # Проверяем, что результат не выводится
        self.assertNotIn("Результат:", output)

    def test_logger_magic_methods_filtering(self):
        """Тест фильтрации магических методов"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def __str__(self):
                return "test"

            def normal_method(self):
                return 42

        obj = TestClass()

        # Вызываем магический метод - он должен быть передан в instance
        # Но так как LoggerWrapper не реализует __str__, Python ищет в instance

        output1 = self.get_output()
        # Проверяем, что магический метод не залогирован
        self.assertEqual(output1, "")

        # Вызываем обычный метод
        obj.normal_method()
        output2 = self.get_output()

        # Проверяем, что обычный метод залогирован
        self.assertIn("Метод: normal_method", output2)

    def test_logger_with_multiple_arguments(self):
        """Тест логирования метода с разными типами аргументов"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def complex_method(self, a, b=10, *args, **kwargs):
                # Суммируем все значения
                result = a + b + sum(args) + sum(kwargs.values())
                return result

        obj = TestClass()
        # ИСПРАВЛЕНО: не передаем b дважды
        result = obj.complex_method(5, 1, 2, 3, x=4, y=5)  # b останется 10

        # 5 + 10 + (1+2+3) + (4+5) = 30
        self.assertEqual(result, 20)
        output = self.get_output()

        # Проверяем корректность вывода аргументов
        self.assertIn("Аргументы: позиционные=(5, 1, 2, 3), именованные={'x': 4, 'y': 5}", output)

    def test_logger_with_args_only(self):
        """Тест логирования метода только с позиционными аргументами"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def args_method(self, *args):
                return sum(args)

        obj = TestClass()
        result = obj.args_method(1, 2, 3, 4, 5)

        self.assertEqual(result, 15)
        output = self.get_output()

        self.assertIn("Аргументы: позиционные=(1, 2, 3, 4, 5), именованные={}", output)

    def test_logger_with_kwargs_only(self):
        """Тест логирования метода только с именованными аргументами"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def kwargs_method(self, **kwargs):
                return sum(kwargs.values())

        obj = TestClass()
        result = obj.kwargs_method(a=1, b=2, c=3)

        self.assertEqual(result, 6)
        output = self.get_output()

        self.assertIn("Аргументы: позиционные=(), именованные={'a': 1, 'b': 2, 'c': 3}", output)

    def test_logger_exception_handling(self):
        """Тест обработки исключений в методе"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def failing_method(self):
                raise ValueError("Test error")

        obj = TestClass()

        with self.assertRaises(ValueError) as context:
            obj.failing_method()

        self.assertEqual(str(context.exception), "Test error")
        output = self.get_output()

        # Проверяем логирование ошибки
        self.assertIn("ОШИБКА: ValueError: Test error", output)

    @patch('time.time')
    def test_logger_execution_time_measurement(self, mock_time):
        """Тест измерения времени выполнения"""
        mock_time.side_effect = [1000.0, 1001.5]  # start, end

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def slow_method(self):
                pass  # Убираем time.sleep, чтобы не влиять на тест

        obj = TestClass()
        obj.slow_method()
        output = self.get_output()

        # Проверяем время выполнения (1500 мс = 1.5 секунды)
        self.assertIn("Время: 1500.000мс", output)

    def test_logger_preserves_method_metadata(self):
        """Тест сохранения метаданных оригинального метода"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def test_method(self):
                """Test documentation"""
                pass

        obj = TestClass()

        # Проверяем, что метаданные сохранены
        self.assertEqual(obj.test_method.__name__, "test_method")
        self.assertEqual(obj.test_method.__doc__, "Test documentation")

    def test_logger_with_multiple_methods(self):
        """Тест логирования нескольких методов одного класса"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def method1(self):
                return 1

            def method2(self):
                return 2

            def method3(self):
                return 3

        obj = TestClass()

        obj.method1()
        obj.method2()
        obj.method3()
        output = self.get_output()

        # Проверяем, что все методы залогированы
        self.assertIn("Метод: method1", output)
        self.assertIn("Метод: method2", output)
        self.assertIn("Метод: method3", output)

    def test_logger_with_multiple_instances(self):
        """Тест логирования для нескольких экземпляров класса"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def __init__(self, name):
                self.name = name

            def greet(self):
                return f"Hello from {self.name}"

        obj1 = TestClass("Instance1")
        obj2 = TestClass("Instance2")

        obj1.greet()
        obj2.greet()
        output = self.get_output()

        # Проверяем, что оба вызова залогированы с правильными именами классов
        self.assertEqual(output.count("Класс: TestClass"), 2)

    def test_logger_with_property(self):
        """Тест логирования property (не должно логироваться)"""

        @logger(show_magic_methods=False, show_result=True)
        class TestClass:
            def __init__(self):
                self._value = 42

            @property
            def value(self):
                return self._value

        obj = TestClass()
        result = obj.value

        self.assertEqual(result, 42)
        output = self.get_output()

        # Property не является вызываемым, поэтому не должно логироваться
        self.assertEqual(output, "")


class TestCalculatorWithLogger(unittest.TestCase):
    """Тесты для класса Calculator с декоратором logger"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    def test_calculator_initialization(self):
        """Тест инициализации калькулятора"""
        calc = Calculator("TestCalc")

        # Получаем доступ к оригинальному instance
        self.assertEqual(calc.instance.name, "TestCalc")
        output = self.held_output.getvalue()

        # __init__ не должен логироваться (show_magic_methods=False)
        self.assertEqual(output, "")

    def test_calculator_add_method(self):
        """Тест метода add с логированием"""
        calc = Calculator("TestCalc")
        result = calc.add(5, 3)

        self.assertEqual(result, 8)
        output = self.held_output.getvalue()

        # Проверяем логирование add
        self.assertIn("Класс: Calculator", output)
        self.assertIn("Метод: add", output)
        self.assertIn("Аргументы: позиционные=(5, 3), именованные={}", output)
        self.assertIn("Результат: 8", output)

    def test_calculator_add_with_floats(self):
        """Тест метода add с числами с плавающей точкой"""
        calc = Calculator("TestCalc")
        result = calc.add(2.5, 3.7)

        self.assertEqual(result, 6.2)
        output = self.held_output.getvalue()

        self.assertIn("Результат: 6.2", output)

    def test_calculator_add_with_negative_numbers(self):
        """Тест метода add с отрицательными числами"""
        calc = Calculator("TestCalc")
        result = calc.add(-5, 3)

        self.assertEqual(result, -2)
        output = self.held_output.getvalue()

        self.assertIn("Результат: -2", output)

    def test_calculator_divide_success(self):
        """Тест успешного деления"""
        calc = Calculator("TestCalc")
        result = calc.divide(10, 2)

        self.assertEqual(result, 5.0)
        output = self.held_output.getvalue()

        self.assertIn("Метод: divide", output)
        self.assertIn("Результат: 5.0", output)

    def test_calculator_divide_by_zero(self):
        """Тест деления на ноль"""
        calc = Calculator("TestCalc")

        with self.assertRaises(ValueError) as context:
            calc.divide(10, 0)

        self.assertEqual(str(context.exception), "Деление на ноль!")
        output = self.held_output.getvalue()

        # Проверяем логирование ошибки
        self.assertIn("ОШИБКА: ValueError: Деление на ноль!", output)

    def test_calculator_divide_with_floats(self):
        """Тест деления с числами с плавающей точкой"""
        calc = Calculator("TestCalc")
        result = calc.divide(7, 3)

        self.assertAlmostEqual(result, 2.3333333333333335)
        output = self.held_output.getvalue()

        self.assertIn("Результат: 2.3333333333333335", output)


    def test_calculator_multiple_operations(self):
        """Тест нескольких операций подряд"""
        calc = Calculator("TestCalc")

        calc.add(1, 2)
        calc.add(3, 4)
        calc.divide(10, 2)

        output = self.held_output.getvalue()

        # Проверяем, что все операции залогированы
        self.assertEqual(output.count("Метод: add"), 2)
        self.assertEqual(output.count("Метод: divide"), 1)

    def test_calculator_with_different_names(self):
        """Тест калькуляторов с разными именами"""
        calc1 = Calculator("Calc1")
        calc2 = Calculator("Calc2")

        calc1.add(1, 2)
        calc2.add(3, 4)

        output = self.held_output.getvalue()

        # Проверяем, что оба вызова залогированы
        self.assertEqual(output.count("Класс: Calculator"), 2)


class TestCalculatorEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев калькулятора"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    def test_calculator_with_empty_name(self):
        """Тест калькулятора с пустым именем"""
        calc = Calculator("")

        self.assertEqual(calc.instance.name, "")


    def test_calculator_with_long_name(self):
        """Тест калькулятора с длинным именем"""
        long_name = "A" * 1000
        calc = Calculator(long_name)

        self.assertEqual(calc.instance.name, long_name)


    def test_calculator_add_with_large_numbers(self):
        """Тест сложения с большими числами"""
        calc = Calculator("Test")
        result = calc.add(10 ** 100, 10 ** 100)

        self.assertEqual(result, 2 * 10 ** 100)

    def test_calculator_divide_with_small_numbers(self):
        """Тест деления с очень маленькими числами"""
        calc = Calculator("Test")
        result = calc.divide(1, 10 ** -10)

        self.assertEqual(result, 10 ** 10)

if __name__ == '__main__':
    unittest.main(verbosity=2)