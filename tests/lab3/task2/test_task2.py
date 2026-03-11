import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../lab3/task2')))

from lab3.task2.main import collect_items, create_file


class TestCollectItems(unittest.TestCase):
    """Тесты для функции collect_items"""

    def setUp(self):
        """Подготовка перед тестом"""
        self.test_dir = tempfile.mkdtemp()

        # Создаём структуру папок
        os.makedirs(os.path.join(self.test_dir, "folder1", "subfolder1"))
        os.makedirs(os.path.join(self.test_dir, "folder1", "subfolder2"))
        os.makedirs(os.path.join(self.test_dir, "folder2"))
        os.makedirs(os.path.join(self.test_dir, "folder3", "subfolder3", "deep"))

        # Создаём несколько файлов
        with open(os.path.join(self.test_dir, "file1.txt"), "w") as f:
            f.write("test")
        with open(os.path.join(self.test_dir, "folder1", "file2.txt"), "w") as f:
            f.write("test")

    def tearDown(self):
        """Очистка после теста"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_collect_items(self):
        """Тест сбора всех папок"""
        # Вызываем функцию
        folders = collect_items(self.test_dir)

        # Ожидаемые папки
        expected_folders = [
            os.path.join(self.test_dir, "folder1"),
            os.path.join(self.test_dir, "folder1", "subfolder1"),
            os.path.join(self.test_dir, "folder1", "subfolder2"),
            os.path.join(self.test_dir, "folder2"),
            os.path.join(self.test_dir, "folder3"),
            os.path.join(self.test_dir, "folder3", "subfolder3"),
            os.path.join(self.test_dir, "folder3", "subfolder3", "deep"),
        ]

        self.assertEqual(len(folders), len(expected_folders))

        # Проверяем наличие всех папок
        for folder in expected_folders:
            self.assertIn(folder, folders)


class TestCreateFile(unittest.TestCase):
    """Тесты для функции create_file"""

    def setUp(self):
        """Подготовка перед тестом"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Очистка после теста"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_file(self):
        """Тест создания файла с содержимым"""
        test_filename = "test_create.txt"

        # Вызываем функцию
        create_file(test_filename)

        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(test_filename))

        # Проверяем содержимое файла
        with open(test_filename, 'rb') as f:
            content = f.read()
            self.assertEqual(content, test_filename.encode("utf-8"))

        # Проверяем размер файла
        file_size = os.path.getsize(test_filename)
        self.assertEqual(file_size, len(test_filename))


if __name__ == '__main__':
    unittest.main()
