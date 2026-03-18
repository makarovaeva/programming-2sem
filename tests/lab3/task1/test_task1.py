import unittest
import datetime
import os
import stat
import tempfile
import shutil
from io import StringIO
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../lab3/task1'))
from lab3.task1.main import convert_to_date, print_access, main


class TestConvertToDate(unittest.TestCase):
    """Тесты для функции convert_to_date"""

    def test_convert_to_date(self):
        """Тест преобразования timestamp в datetime"""
        test_timestamp = 1609459200  # 2021-01-01
        result = convert_to_date(test_timestamp)

        self.assertIsInstance(result, datetime.datetime)
        self.assertEqual(result.year, 2021)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)


class TestIsAccess(unittest.TestCase):
    """Тесты для функции is_access"""

    def test_is_access_output(self):
        """Тест вывода функции is_access"""
        # Сохраняем оригинальный stdout
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Вызываем функцию
        access_string = "110110100"
        print_access(access_string)

        # Получаем вывод
        output = sys.stdout.getvalue()

        # Восстанавливаем stdout
        sys.stdout = original_stdout

        # Проверяем с учётом форматирования
        self.assertIn("Права доступа для владельца: 110", output)
        self.assertIn("Права доступа для группы:", output)
        self.assertIn("110", output)  # Проверяем, что 110 где-то есть
        self.assertIn("Права доступа для остальных: 100", output)
        self.assertIn("rwx", output)


class TestMainFunction(unittest.TestCase):
    """Тесты для функции main с реальными файлами"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file_name = "test_file.txt"
        self.test_file_path = os.path.join(self.test_dir, self.test_file_name)

    def tearDown(self):
        """Очистка после каждого теста"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_main_creates_file(self):
        """Тест 1: Проверка, что main создаёт файл"""
        # Запускаем main с параметрами
        try:
            main(self.test_dir, self.test_file_name)
        except Exception as e:
            self.fail(f"main вызвал исключение: {e}")

        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(self.test_file_path))
        self.assertTrue(os.path.isfile(self.test_file_path))

    def test_main_file_content(self):
        """Тест 2: Проверка содержимого созданного файла"""
        # Запускаем main
        try:
            main(self.test_dir, self.test_file_name)
        except Exception as e:
            self.fail(f"main вызвал исключение: {e}")

        # Проверяем содержимое файла
        with open(self.test_file_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b"File for task 1")

    def test_main_file_size(self):
        """Тест 3: Проверка размера созданного файла"""
        # Запускаем main
        try:
            main(self.test_dir, self.test_file_name)
        except Exception as e:
            self.fail(f"main вызвал исключение: {e}")

        # Проверяем размер файла
        file_size = os.path.getsize(self.test_file_path)
        expected_size = len(b"File for task 1")
        self.assertEqual(file_size, expected_size)

    def test_main_deletes_existing_file(self):
        """Тест 4: Проверка удаления существующего файла"""
        # Создаём существующий файл
        with open(self.test_file_path, 'w') as f:
            f.write("old content")

        # Запускаем main
        try:
            main(self.test_dir, self.test_file_name)
        except Exception as e:
            self.fail(f"main вызвал исключение: {e}")

        # Проверяем, что новый файл содержит правильные данные
        with open(self.test_file_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b"File for task 1")

    def test_main_readonly_handling(self):
        """Тест 5: Проверка обработки read-only файла"""
        # Создаём файл с атрибутом "только для чтения"
        with open(self.test_file_path, 'w') as f:
            f.write("readonly content")

        # Устанавливаем атрибут "только для чтения"
        os.chmod(self.test_file_path, stat.S_IREAD)

        # Запускаем main
        try:
            main(self.test_dir, self.test_file_name)
        except Exception as e:
            self.fail(f"main вызвал исключение при обработке read-only файла: {e}")

        # Проверяем, что файл содержит новые данные
        with open(self.test_file_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b"File for task 1")


if __name__ == '__main__':
    unittest.main()
