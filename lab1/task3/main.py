from lab1.task3.calculator import Calculator

if __name__ == '__main__':
    """
    Точка входа для демонстрации работы декоратора logger на классе Calculator.

    Этот скрипт создает экземпляр класса Calculator и вызывает его методы
    для демонстрации логирования, которое обеспечивает декоратор @logger.

    Декоратор настроен с параметрами:
        show_magic_methods=False - магические методы не логируются
        show_result=True - результат выполнения выводится в лог
    """

    # Создание экземпляра класса Calculator
    # __init__ не логируется (show_magic_methods=False)
    calc = Calculator("Калькулятор 3000")

    # Будет залогирован с результатом (show_result=True)
    calc.add(1, 2)

    calc.divide(10, 0)  # Вызовет ValueError и будет залогировано исключение