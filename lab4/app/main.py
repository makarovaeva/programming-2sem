import sys

from database import DataBase
from database_manager import DataBaseManager


def main() -> None:
    """
    Точка входа в программу для запуска менеджера работы с БД.

    Функция создает экземпляр классов DataBase, DataBaseManager и запускает его основной цикл.
    Обрабатывает возможные исключения:
    - KeyboardInterrupt: при прерывании программы пользователем (Ctrl+C)
    - Exception: все остальные критические ошибки

    Args:
        None: Функция не принимает аргументов.

    Returns:
        None: Функция ничего не возвращает.

    Raises:
        Не выбрасывает исключений наружу, все ошибки обрабатываются внутри.
    """
    db = DataBase()
    db_manager = DataBaseManager(db)
    try:
        db_manager.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
        db.close()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        db.close()
        sys.exit(1)


if __name__ == "__main__":
    """Точка входа"""
    main()
