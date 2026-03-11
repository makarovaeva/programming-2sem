from lab1.task4.printer import Printer

if __name__ == '__main__':
    """
    Скрипт для демонстрации работы декоратора limiter на классе Printer.

    Этот скрипт создает экземпляр класса Printer с ограничением на 3 вызова
    каждого метода (декоратор @limiter(limit=3)) и пытается вызвать методы
    print_greeting() и print_message() 4 раза в цикле.

    Декоратор limiter настроен с параметром:
        limit=3 - максимальное количество вызовов для каждого метода
    """

    printer = Printer("Принтер 3000")

    for i in range(4):
        print(f"\nИтерация {i + 1}")

        # Вызов метода print_greeting (на 4-й итерации будет ошибка)
        printer.print_greeting()

        # Вызов метода print_message (на 4-й итерации будет ошибка)
        printer.print_message("bye")