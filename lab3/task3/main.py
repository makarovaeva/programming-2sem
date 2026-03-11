import sys

from lab3.task3.system_manager import SystemManager


def main() -> None:
    """
    Точка входа в программу для запуска менеджера системы.

    Функция создает экземпляр класса SystemManager и запускает его основной цикл.
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
    try:
        manager = SystemManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """Точка входа"""
    main()