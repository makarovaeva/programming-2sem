import datetime
import os
import stat


def convert_to_date(ms: float) -> datetime.datetime:
    """
    Преобразует временную метку в объект datetime.

    Args:
        ms (float): Временная метка в секундах с начала эпохи (timestamp).

    Returns:
        datetime.datetime: Объект datetime, представляющий дату и время.
    """
    return datetime.datetime.fromtimestamp(ms)


def is_access(access: str) -> None:
    """
    Анализирует и выводит права доступа к файлу в символьном формате.

    Функция принимает строку из 9 символов (битов прав доступа) и
    разбивает её на три группы по 3 символа: для владельца, группы и остальных.
    Каждая группа представляет права на чтение (r), запись (w) и исполнение (x).

    Args:
        access (str): Строка из 9 символов, представляющая биты прав доступа.

    Returns:
        None: Функция ничего не возвращает, только выводит информацию.
    """
    owner = access[:3]
    group = access[3:6]
    others = access[6:]

    print("rwx".rjust(32))
    print(f"Права доступа для владельца: {owner}")
    print(f"Права доступа для группы: {group.rjust(6)}")
    print(f"Права доступа для остальных: {others}")


def main(path: str, file_name: str) -> None:
    """
    Главная функция программы.

    Выполняет следующие действия:
    1. Формирует полный путь к файлу из глобальных переменных path и file_name.
    2. Если файл уже существует, снимает с него атрибут "только для чтения"
       и удаляет его.
    3. Создаёт новый файл и записывает в него числа от 0 до 99.
    4. Проверяет существование файла и выводит сообщение.
    5. Получает информацию о файле через os.stat().
    6. Выводит размер файла, даты последнего изменения и доступа.
    7. Выводит имя текущего пользователя через os.getlogin().
    8. Выводит имя пользователя из переменных окружения.
    9. Отображает права доступа до изменения.
    10. Устанавливает атрибут "только для чтения" (stat.S_IREAD).
    11. Обновляет информацию о файле и снова отображает права доступа.

    Args:
        path (str): Путь к директории для работы с файлом
        file_name (str): Имя файла для работы

    Returns:
        None: Функция ничего не возвращает.
    """
    file = os.path.join(path, file_name)

    # Удаляем существующий файл, если он есть
    if os.path.exists(file):
        os.chmod(file, stat.S_IWRITE)  # Снимаем read-only атрибут
        os.remove(file)

    # Создаём новый файл и записываем данные
    fd = os.open(file, os.O_CREAT | os.O_WRONLY)
    os.write(fd, b"File for task 1")
    os.close(fd)

    if os.path.exists(file):
        print("Файл существует")

    # Получаем информацию о файле
    file_info = os.stat(file)

    print(f"Размер файла в байтах: {file_info.st_size}")
    print(f"Дата последнего изменения: {convert_to_date(file_info.st_mtime)}")
    print(f"Дата последнего доступа: {convert_to_date(file_info.st_atime)}")

    # Информация о пользователе
    print(f"Текущий пользователь: {os.getlogin()}")

    # Анализ прав доступа до изменения
    mode = f"{file_info.st_mode:b}"
    print("\nДо изменения прав доступа:")
    is_access(mode[7:])  # Берём последние 9 бит

    # Изменяем права на "только для чтения"
    os.chmod(file, stat.S_IREAD)

    # Обновляем информацию о файле
    file_info = os.stat(file)

    # Анализ прав доступа после изменения
    mode = f"{file_info.st_mode:b}"
    print("\nПосле изменения прав доступа:")
    is_access(mode[7:])


if __name__ == '__main__':
    """
    Точка входа в программу.

    Определяет глобальные переменные path и file_name,
    затем запускает главную функцию main().
    """
    path = os.getcwd()
    file_name = "file_task1.txt"
    main()