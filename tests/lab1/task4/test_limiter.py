import unittest
import io
import sys
from lab1.task4.call_limiter import call_limiter
from lab1.task4.printer import Printer


class TestLimiterDecorator(unittest.TestCase):
    """Тесты для декоратора limiter"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 1: Проверка создания декоратора с некорректным лимитом
    def test_limiter_invalid_limit(self):
        """Тест 1: Проверка вызова исключения при limit < 1"""

        with self.assertRaises(ValueError) as context:
            @call_limiter(limit=0)
            class TestClass:
                def method(self):
                    pass

        self.assertEqual(str(context.exception), "Лимит вызовов должен быть больше 0")

        with self.assertRaises(ValueError):
            @call_limiter(limit=-5)
            class TestClass:
                pass

    # ТЕСТ 2: Проверка базового ограничения вызовов
    def test_limiter_basic_limit(self):
        """Тест 2: Проверка базового ограничения количества вызовов"""

        @call_limiter(limit=2)
        class TestClass:
            def method(self):
                return "OK"

        obj = TestClass()

        # Первые два вызова должны работать
        self.assertEqual(obj.method(), "OK")
        self.assertEqual(obj.method(), "OK")

        # Третий вызов должен вызвать исключение
        with self.assertRaises(RuntimeError) as context:
            obj.method()

        self.assertIn("превысил лимит вызовов (2)", str(context.exception))
        self.assertIn("Попытка вызова #3", str(context.exception))

    # ТЕСТ 3: Проверка независимости счетчиков для разных методов
    def test_limiter_different_methods_independent(self):
        """Тест 3: Проверка независимости счетчиков для разных методов одного экземпляра"""

        @call_limiter(limit=2)
        class TestClass:
            def method1(self):
                return 1

            def method2(self):
                return 2

        obj = TestClass()

        # Вызываем method1 2 раза (до лимита)
        obj.method1()
        obj.method1()

        # method2 должен быть доступен
        self.assertEqual(obj.method2(), 2)
        self.assertEqual(obj.method2(), 2)

        # method2 тоже должен превысить лимит
        with self.assertRaises(RuntimeError):
            obj.method2()

    # ТЕСТ 4: Проверка независимости счетчиков для разных экземпляров
    def test_limiter_different_instances_independent(self):
        """Тест 4: Проверка независимости счетчиков для разных экземпляров класса"""

        @call_limiter(limit=2)
        class TestClass:
            def method(self):
                return "OK"

        obj1 = TestClass()
        obj2 = TestClass()

        # obj1 исчерпывает лимит
        obj1.method()
        obj1.method()

        with self.assertRaises(RuntimeError):
            obj1.method()

        # obj2 должен иметь свои счетчики
        self.assertEqual(obj2.method(), "OK")
        self.assertEqual(obj2.method(), "OK")

        with self.assertRaises(RuntimeError):
            obj2.method()


    # ТЕСТ 8: Проверка сохранения метаданных методов
    def test_limiter_preserves_metadata(self):
        """Тест 8: Проверка сохранения метаданных оригинальных методов"""

        @call_limiter(limit=2)
        class TestClass:
            def method(self):
                """Тестовая документация"""
                pass

        obj = TestClass()

        self.assertEqual(obj.method.__name__, "method")
        self.assertEqual(obj.method.__doc__, "Тестовая документация")


class TestPrinterWithLimiter(unittest.TestCase):
    """Тесты для класса Printer с декоратором limiter"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 9: Проверка работы класса Printer с лимитом
    def test_printer_basic_functionality(self):
        """Тест 9: Проверка базовой функциональности класса Printer с лимитом 3"""

        printer = Printer("Тестовый")


        # Вызываем методы в пределах лимита
        for i in range(3):
            printer.print_greeting()
            printer.print_message(f"сообщение {i + 1}")

        output = self.held_output.getvalue()

        # Проверяем вывод
        self.assertIn("Привет от Тестовый!", output)
        self.assertIn("[Тестовый] сообщение 1", output)
        self.assertIn("[Тестовый] сообщение 2", output)
        self.assertIn("[Тестовый] сообщение 3", output)
        self.assertEqual(output.count("Привет от Тестовый!"), 3)
        self.assertEqual(output.count("[Тестовый] сообщение"), 3)

        # Очищаем вывод
        self.held_output.truncate(0)
        self.held_output.seek(0)

        # Превышаем лимит для print_greeting
        with self.assertRaises(RuntimeError) as context_g:
            printer.print_greeting()

        self.assertIn("print_greeting", str(context_g.exception))
        self.assertIn("превысил лимит вызовов (3)", str(context_g.exception))

        # Превышаем лимит для print_message
        with self.assertRaises(RuntimeError) as context_m:
            printer.print_message("ещё одно")

        self.assertIn("print_message", str(context_m.exception))

    # ТЕСТ 10: Проверка служебных методов для Printer
    def test_printer_utility_methods(self):
        """Тест 10: Проверка служебных методов (get_call_stats, reset_call_counters, can_call) для Printer"""

        printer = Printer("Служебный")

        # Изначально все методы доступны
        self.assertTrue(printer.can_call('print_greeting'))
        self.assertTrue(printer.can_call('print_message'))

        # Вызываем методы
        printer.print_greeting()
        printer.print_message("тест")
        printer.print_greeting()

        # Проверяем статистику
        stats = printer.get_call_stats()
        self.assertEqual(stats['print_greeting'], 2)
        self.assertEqual(stats['print_message'], 1)

        # Проверяем доступность
        self.assertTrue(printer.can_call('print_greeting'))  # еще можно (3-й вызов)
        self.assertTrue(printer.can_call('print_message'))  # еще можно (2-й и 3-й)

        # Вызываем до лимита
        printer.print_greeting()  # 3-й вызов
        printer.print_message("тест2")
        printer.print_message("тест3")

        # Проверяем недоступность
        self.assertFalse(printer.can_call('print_greeting'))
        self.assertFalse(printer.can_call('print_message'))

        # Статистика после лимита
        stats = printer.get_call_stats()
        self.assertEqual(stats['print_greeting'], 3)
        self.assertEqual(stats['print_message'], 3)

        # Сбрасываем счетчики
        printer.reset_call_counters()

        # После сброса методы снова доступны
        self.assertTrue(printer.can_call('print_greeting'))
        self.assertTrue(printer.can_call('print_message'))

        # Статистика после сброса
        stats = printer.get_call_stats()
        self.assertEqual(stats.get('print_greeting', 0), 0)
        self.assertEqual(stats.get('print_message', 0), 0)

        # Снова можно вызывать
        printer.print_greeting()
        printer.print_message("после сброса")

        output = self.held_output.getvalue()
        self.assertIn("Привет от Служебный!", output)
        self.assertIn("[Служебный] после сброса", output)


class TestLimiterAdvancedFeatures(unittest.TestCase):
    """Тесты для дополнительных возможностей декоратора limiter"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout
        self.held_output.close()

    # ТЕСТ 11 (дополнительный): Проверка работы с методами, принимающими аргументы
    def test_limiter_with_arguments(self):
        """Тест 11: Проверка работы с методами, принимающими различные аргументы"""

        @call_limiter(limit=2)
        class TestClass:
            def sum(self, a, b):
                return a + b

            def greet(self, name, greeting="Hello"):
                return f"{greeting}, {name}!"

        obj = TestClass()

        # Вызываем с разными аргументами
        self.assertEqual(obj.sum(5, 3), 8)
        self.assertEqual(obj.sum(10, 20), 30)

        # Лимит должен считаться по количеству вызовов, не по аргументам
        with self.assertRaises(RuntimeError):
            obj.sum(1, 1)

        # Другой метод должен быть доступен
        self.assertEqual(obj.greet("Alice"), "Hello, Alice!")
        self.assertEqual(obj.greet("Bob", "Hi"), "Hi, Bob!")

        with self.assertRaises(RuntimeError):
            obj.greet("Charlie")

    # ТЕСТ 12 (дополнительный): Проверка сброса только для одного экземпляра
    def test_limiter_reset_one_instance(self):
        """Тест 12: Проверка, что сброс счетчиков работает только для конкретного экземпляра"""

        @call_limiter(limit=2)
        class TestClass:
            def method(self):
                return "OK"

        obj1 = TestClass()
        obj2 = TestClass()

        # obj1 исчерпывает лимит
        obj1.method()
        obj1.method()

        # obj2 еще не вызывался
        obj2.method()

        # Сбрасываем obj1
        obj1.reset_call_counters()

        # obj1 снова может вызывать
        obj1.method()

        # obj2 все еще имеет свои счетчики
        obj2.method()  # второй вызов

        with self.assertRaises(RuntimeError):
            obj2.method()  # третий вызов - ошибка

        # obj1 после сброса должен работать
        obj1.method()  # второй вызов после сброса

        # Проверяем статистику
        self.assertEqual(obj1.get_call_stats()['method'], 2)
        self.assertEqual(obj2.get_call_stats()['method'], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)