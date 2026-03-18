import os
import stat


def print_dir(directory: str) -> None:
    """
    Выводит содержимое указанной директории.

    Функция переходит в указанную директорию и выводит список всех файлов и папок,
    находящихся в ней. Перед выводом выводится заголовок с путём к директории.

    Args:
        directory (str): Путь к директории, содержимое которой нужно вывести.

    Returns:
        None: Функция ничего не возвращает, только выводит информацию.
    """
    print(f"\nФайлы и папки директории: {directory}")
    for item in os.listdir():
        print(item)


def copy_file(buffer_size: int = 1024 * 1024) -> bool:
    """
    Копирует файл из исходного пути в целевой с использованием низкоуровневых операций.

    Функция открывает исходный файл для чтения и целевой файл для записи,
    затем копирует данные блоками указанного размера. Используются системные вызовы
    os.open(), os.read(), os.write() для максимальной производительности.

    Args:
        buffer_size (int, optional): Размер буфера для копирования в байтах.
                                     По умолчанию 1 МБ (1024 * 1024).
                                     Меньший размер экономит память,
                                     больший - увеличивает скорость.

    Returns:
        bool: True если копирование успешно, False в противном случае.

    Raises:
        Не выбрасывает исключений, все ошибки перехватываются и выводятся в консоль.
    """
    if not os.path.exists(src_file):
        return False

    try:
        src_fd = os.open(src_file, os.O_RDONLY)

        dst_fd = os.open(cp_file, os.O_WRONLY | os.O_CREAT)

        # Копируем данные блоками
        while True:
            buffer = os.read(src_fd, buffer_size)
            if not buffer:
                break
            os.write(dst_fd, buffer)

        # Закрываем файловые дескрипторы
        os.close(src_fd)
        os.close(dst_fd)

        return True

    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        return False


def collect_items(start_path: str) -> list:
    """
    Рекурсивно собирает все папки в указанной директории и её поддиректориях.

    Функция использует os.walk() для рекурсивного обхода дерева каталогов
    и собирает полные пути ко всем папкам.

    Args:
        start_path (str): Начальный путь для рекурсивного поиска папок.

    Returns:
        list: Список строк с полными путями ко всем найденным папкам.
    """
    folders = []

    for root, dirs, filenames in os.walk(start_path):
        for dir_name in dirs:
            folders.append(os.path.join(root, dir_name))

    return folders


def print_collection(folders: list) -> None:
    """
    Выводит собранные папки и их содержимое.

    Функция выводит список всех найденных папок, затем для каждой папки
    переходит в неё и выводит список файлов, находящихся непосредственно в ней.

    Args:
        folders (list): Список строк с путями к папкам.

    Returns:
        None: Функция ничего не возвращает, только выводит информацию.
    """
    print(f"\nНайдено папок: {len(folders)}")
    for folder in sorted(folders):
        print(folder)

    for folder in sorted(folders):
        print(f"\nФайлы в папке {os.path.basename(folder)}")
        os.chdir(folder)
        for item in os.listdir():
            if os.path.isfile(item):
                print(item)


def create_file(f_name: str) -> None:
    """
    Создает файловый дескриптор с правами на запись по имени f_name,
    записывает в файл имя f_name, закрывает файловый дескриптор.

    :param f_name: str
    :return: None
    """
    fd = os.open(f_name, os.O_CREAT | os.O_WRONLY)
    os.write(fd, f_name.encode("utf-8"))
    os.close(fd)


def main() -> None:
    """
    Главная функция программы, выполняющая последовательность операций.

    Выполняет следующие действия в рамках лабораторной работы:

    1. Копирование файла:
       - Копирует файл из task1/file_task1.txt в текущую директорию
       - Использует функцию copy_file()

    2. Переименование и перемещение:
       - Переименовывает скопированный файл в file_task2.txt
       - Создаёт папки folder1 и folder2
       - Перемещает файл в folder1/folder2/
       - Меняет права доступа для возможности перемещения

    3. Создание и переименование нового файла:
       - Создаёт old_name.txt с содержимым
       - Перемещает и переименовывает его в folder1/folder2/new_name.txt

    4. Создание нескольких файлов и просмотр директорий:
       - Создаёт файлы file_№1, file_№2, file_№3
       - Выводит содержимое текущей директории и folder1/folder2

    5. Создание и удаление папок:
       - Создаёт и сразу удаляет empty_folder
       - Создаёт папки folder3-folder7 с файлами внутри

    6. Рекурсивный сбор информации:
       - Собирает все папки начиная с текущей директории
       - Выводит собранные папки и файлы в них

    Args:
        None: Функция не принимает аргументов, использует глобальные переменные.

    Returns:
        None: Функция ничего не возвращает.

    Raises:
        Exception: Может возникать при ошибках файловых операций,
                  но все ошибки обрабатываются внутри функций.
    """
    # Часть 1: Копирование файла
    if not copy_file():
        return

    # Часть 2: Переименование и перемещение
    new_name = os.path.join(cur_path, "file_task2.txt")
    if not os.path.exists(new_name):
        os.rename(cp_file, new_name)

    # Создание папок folder1 и folder2
    if not os.path.exists("folder1"):
        os.mkdir("folder1")

    os.chdir("folder1")

    if not os.path.exists("folder2"):
        os.mkdir("folder2")

    # Перемещение файла в folder1/folder2
    os.chmod(new_name, stat.S_IWUSR)
    path_to_folder2 = os.path.join(cur_path, r"folder1\folder2")
    os.replace(new_name, os.path.join(path_to_folder2, "file_task2.txt"))

    # Часть 3: Создание и переименование нового файла
    name = "old_name.txt"
    create_file(name)

    new_path = os.path.join(path_to_folder2, "new_name.txt")
    if not os.path.exists(new_path):
        os.rename(name, new_path)

    # Часть 4: Создание нескольких файлов и просмотр директорий
    os.chdir(cur_path)
    for i in range(1, 4):
        create_file(f"file_№{i}.txt")

    print_dir(cur_path)
    os.chdir(path_to_folder2)
    print_dir(path_to_folder2)

    # Часть 5: Создание и удаление папок
    os.chdir(cur_path)
    ef = "empty_folder"
    if not os.path.exists(ef):
        os.mkdir(ef)
    os.rmdir(ef)

    # Создание папок folder3-folder7 с файлами внутри
    for i in range(3, 8):
        folder = f"folder{i}"
        if not os.path.exists(folder):
            os.mkdir(folder)
        os.chdir(folder)
        create_file(f"file_in_{folder}.txt")

    # Часть 6: Рекурсивный сбор информации
    folders = collect_items(cur_path)
    print_collection(folders)


if __name__ == '__main__':
    """
    Точка входа в программу.

    Определяет глобальные переменные и запускает главную функцию main().

    Глобальные переменные:
        cur_path (str): Текущая рабочая директория.
        path_task1 (str): Путь к директории task1 (на уровень выше).
        file_name (str): Имя файла для работы.
        src_file (str): Полный путь к исходному файлу для копирования.
        cp_file (str): Полный путь к копируемому файлу в текущей директории.
    """
    cur_path = os.getcwd()  # Текущая директория lab3/task2
    path_task1 = os.path.join(os.path.dirname(cur_path), "task1")  # Путь к task1
    file_name = "file_task1.txt"
    src_file = os.path.join(path_task1, file_name)  # Исходный файл для копирования
    cp_file = os.path.join(cur_path, file_name)  # Целевой файл для копирования
    main()
