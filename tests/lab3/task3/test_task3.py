import os
import sys
import unittest
from io import StringIO


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../lab3/task3')))
from lab3.task3.system_manager import SystemManager, clear_screen, print_header


class TestSystemManager(unittest.TestCase):
    """Тесты для класса SystemManager"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.manager = SystemManager()
        # Сохраняем оригинальный stdout
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout

    def test_init(self):
        """Тест 1: Проверка инициализации SystemManager"""
        self.assertIsNotNone(self.manager)
        self.assertTrue(self.manager.running)
        self.assertIsNotNone(self.manager.current_user)

    def test_show_menu(self):
        """Тест 2: Проверка отображения меню"""
        self.manager.show_menu()
        output = self.captured_output.getvalue()

        # Проверяем наличие ключевых элементов меню
        self.assertIn("МЕНЕДЖЕР СИСТЕМЫ", output)
        self.assertIn("Текущий пользователь:", output)
        self.assertIn("a) Показать все запущенные процессы", output)
        self.assertIn("b) Детальная информация о процессе", output)
        self.assertIn("c) Завершить процесс по PID", output)
        self.assertIn("d) Переменные окружения", output)
        self.assertIn("e) Изменить приоритет процесса", output)
        self.assertIn("f) Информация о системе", output)
        self.assertIn("g) Выход", output)


class TestUtilityFunctions(unittest.TestCase):
    """Тесты для вспомогательных функций"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.original_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.original_stdout

    def test_clear_screen(self):
        """Тест 11: Проверка функции очистки экрана"""
        try:
            clear_screen()
            # Просто проверяем, что функция не вызывает исключений
            self.assertTrue(True)
        except Exception:
            self.fail("clear_screen вызвал исключение")

    def test_print_header(self):
        """Тест 12: Проверка вывода заголовка"""
        test_title = "Тестовый заголовок"
        print_header(test_title)
        output = self.captured_output.getvalue()

        # Проверяем, что заголовок выводится
        self.assertIn(test_title, output)


if __name__ == '__main__':
    unittest.main()
