import os
import platform
from datetime import datetime

import psutil


def print_header(title: str) -> None:
    """Выводит заголовок"""
    print(f"{title:^60}")


def wait_for_enter() -> None:
    """Ждет нажатия Enter"""
    input("\nНажмите Enter для продолжения...")


class SystemManager:
    priority_map = {
        '1': ('IDLE', psutil.IDLE_PRIORITY_CLASS),
        '2': ('BELOW NORMAL', psutil.BELOW_NORMAL_PRIORITY_CLASS),
        '3': ('NORMAL', psutil.NORMAL_PRIORITY_CLASS),
        '4': ('ABOVE NORMAL', psutil.ABOVE_NORMAL_PRIORITY_CLASS),
        '5': ('HIGH', psutil.HIGH_PRIORITY_CLASS)
    }

    def __init__(self):
        self.running = True
        self.current_user = os.getlogin()

    def show_menu(self) -> None:
        """Показывает главное меню"""
        print_header("МЕНЕДЖЕР СИСТЕМЫ")
        print(f"Текущий пользователь: {self.current_user}")
        print(f"Система: {platform.system()} {platform.release()}")
        print("\nВыберите действие:")
        print("  a) Показать все запущенные процессы")
        print("  b) Детальная информация о процессе")
        print("  c) Завершить процесс по PID")
        print("  d) Переменные окружения")
        print("  e) Изменить приоритет процесса (nice)")
        print("  f) Информация о системе")
        print("  g) Выход")

    def list_processes(self) -> None:
        """Показывает список всех процессов"""
        print_header("СПИСОК ПРОЦЕССОВ")

        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'username']):
                try:
                    pinfo = proc.info
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Сортируем по использованию CPU
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)

            print(f"{'PID':<8} {'CPU%':<6} {'MEM%':<6} {'Пользователь':<15} {'Статус':<10} {'Имя'}")

            for proc in processes[:30]:  # Показываем первые 30 процессов
                print(f"{proc['pid']:<8} "
                      f"{proc['cpu_percent'] or 0:<6.1f} "
                      f"{proc['memory_percent'] or 0:<6.1f} "
                      f"{proc['username'][:15]:<15} "
                      f"{proc['status'][:10]:<10} "
                      f"{proc['name'][:30]}")

            print(f"\nВсего процессов: {len(processes)}")

        except Exception:
            pass

        wait_for_enter()

    def show_process_details(self) -> None:
        """Показывает детальную информацию о процессе"""
        print_header("ИНФОРМАЦИЯ О ПРОЦЕССЕ")

        try:
            pid = int(input("Введите PID процесса: "))

            if not psutil.pid_exists(pid):
                print(f"Процесс с PID {pid} не существует")
                wait_for_enter()
                return

            proc = psutil.Process(pid)

            print(f"\nДетальная информация о процессе PID={pid}:")
            print(f"Имя: {proc.name()}")
            print(f"Исполняемый файл: {proc.exe()}")
            print(f"Статус: {proc.status()}")
            print(f"Владелец: {proc.username()}")
            print(f"Запущен: {datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')}")

            # Использование ресурсов
            cpu_percent = proc.cpu_percent(interval=0.5)
            memory_info = proc.memory_info()
            print(f"\nИспользование ресурсов:")
            print(f"  CPU: {cpu_percent:.1f}%")
            print(f"  RAM: {memory_info.rss / 1024 / 1024:.2f} MB")
            print(f"  Виртуальная память: {memory_info.vms / 1024 / 1024:.2f} MB")

            if os.name == 'nt':

                current = proc.nice()
                priority_name = "Unknown"
                for key, (name, value) in self.priority_map.items():
                    if value == current:
                        priority_name = name
                        break
                print(f"Приоритет: {priority_name}")

        except psutil.NoSuchProcess:
            print(f"Ошибка: Процесс с PID {pid} не найден")
        except psutil.AccessDenied:
            print(f"Ошибка: Недостаточно прав для доступа к процессу")
        except ValueError:
            print("Ошибка: Введите корректный PID (число)")
        except Exception as e:
            print(f"Ошибка: {e}")

        wait_for_enter()

    def kill_process(self) -> None:
        """Завершает процесс по PID"""
        print_header("ЗАВЕРШЕНИЕ ПРОЦЕССА")

        try:
            pid = int(input("Введите PID процесса для завершения: "))

            if not psutil.pid_exists(pid):
                print(f"Процесс с PID {pid} не существует")
                wait_for_enter()
                return

            proc = psutil.Process(pid)
            print(f"Процесс: {proc.name()} (PID: {pid})")

            # Проверяем права
            if os.name == 'posix' and os.getuid() != 0 and proc.username() != self.current_user:
                print("Внимание: Вы пытаетесь завершить процесс другого пользователя")
                response = input("Продолжить? (y/n): ")
                if response.lower() != 'y':
                    return

            # Спрашиваем подтверждение
            response = input(f"Завершить процесс {proc.name()} (PID={pid})? (y/n): ")

            if response.lower() == 'y':
                # Пробуем мягко завершить
                try:
                    proc.terminate()
                    proc.wait(timeout=3)
                    print(f"Процесс {pid} успешно завершен")
                except psutil.TimeoutExpired:
                    # Если не завершился, убиваем принудительно
                    print("Процесс не отвечает, принудительное завершение...")
                    proc.kill()
                    print(f"Процесс {pid} принудительно завершен")
                except psutil.AccessDenied:
                    print("Ошибка: Недостаточно прав для завершения процесса")
            else:
                print("Операция отменена")

        except psutil.NoSuchProcess:
            print(f"Ошибка: Процесс с PID {pid} не найден")
        except ValueError:
            print("Ошибка: Введите корректный PID (число)")
        except Exception as e:
            print(f"Ошибка: {e}")

        wait_for_enter()

    def manage_environment(self) -> None:
        """Управление переменными окружения"""
        while True:
            print_header("ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ")

            print("1. Показать все переменные")
            print("2. Добавить/Изменить переменную")
            print("3. Вернуться в главное меню")

            choice = input("Выберите действие (1-3): ")

            if choice == '1':
                self.show_all_env()
            elif choice == '2':
                self.set_env_var()
            elif choice == '3':
                break
            else:
                print("Неверный выбор")
                wait_for_enter()

    def show_all_env(self) -> None:
        """Показывает все переменные окружения"""
        print_header("ВСЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ")

        env_vars = dict(os.environ)
        for key, value in sorted(env_vars.items()):
            print(f"{key}: {value}")

        print(f"\nВсего переменных: {len(env_vars)}")
        wait_for_enter()

    def set_env_var(self):
        """Устанавливает переменную окружения"""
        print_header("ДОБАВЛЕНИЕ/ИЗМЕНЕНИЕ ПЕРЕМЕННОЙ")

        var_name = input("Введите имя переменной: ")
        var_value = input("Введите значение: ")

        os.environ[var_name] = var_value
        print(f"Переменная {var_name} установлена в '{var_value}'")

        wait_for_enter()

    def change_process_priority(self) -> None:
        """Изменяет приоритет процесса"""
        print_header("ИЗМЕНЕНИЕ ПРИОРИТЕТА ПРОЦЕССА")

        try:
            pid = int(input("Введите PID процесса: "))

            if not psutil.pid_exists(pid):
                print(f"Процесс с PID {pid} не существует")
                wait_for_enter()
                return

            proc = psutil.Process(pid)

            if os.name == 'nt':
                current = proc.nice()
                current_name = "Unknown"
                for key, (name, value) in self.priority_map.items():
                    if value == current:
                        current_name = name
                        break

                print(f"Текущий приоритет процесса {proc.name()}: {current_name}")
                print("\nДоступные классы приоритета:")
                print("  1. IDLE (Низкий)")
                print("  2. BELOW NORMAL (Ниже среднего)")
                print("  3. NORMAL (Средний)")
                print("  4. ABOVE NORMAL (Выше среднего)")
                print("  5. HIGH (Высокий)")

                choice = input("Выберите класс приоритета (1-5): ")

                if choice in self.priority_map:
                    name, priority_value = self.priority_map[choice]
                    proc.nice(priority_value)
                    print(f"Приоритет процесса изменен на {name}")
                else:
                    print("Неверный выбор")
        except psutil.AccessDenied:
            print("Недостаточно прав для изменения приоритета")
        except ValueError:
            print("Введите корректные числа")
        except Exception as e:
            print(f"Ошибка: {e}")

        wait_for_enter()

    def show_system_info(self) -> None:
        """Показывает информацию о системе"""
        print_header("ИНФОРМАЦИЯ О СИСТЕМЕ")

        # Основная информация
        print("СИСТЕМА:")
        print(f"  ОС: {platform.system()} {platform.release()}")
        print(f"  Версия: {platform.version()}")
        print(f"  Архитектура: {platform.machine()}")
        print(f"  Имя хоста: {platform.node()}")
        print(f"  Процессор: {platform.processor()}")

        # Информация о CPU
        print(f"\nПРОЦЕССОР:")
        print(f"  Ядер (физических): {psutil.cpu_count(logical=False)}")
        print(f"  Ядер (логических): {psutil.cpu_count(logical=True)}")
        print(f"  Частота: {psutil.cpu_freq().current:.0f} МГц")
        print(f"  Загрузка: {psutil.cpu_percent(interval=0.5)}%")

        # Информация о памяти
        mem = psutil.virtual_memory()
        print(f"\nПАМЯТЬ:")
        print(f"  Всего: {mem.total / (1024 ** 3):.2f} GB")
        print(f"  Доступно: {mem.available / (1024 ** 3):.2f} GB")
        print(f"  Используется: {mem.percent}%")

        wait_for_enter()

    def run(self) -> None:
        """Запускает главный цикл программы"""
        while self.running:
            self.show_menu()
            choice = input("Ваш выбор: ").lower()

            if choice == 'a':
                self.list_processes()
            elif choice == 'b':
                self.show_process_details()
            elif choice == 'c':
                self.kill_process()
            elif choice == 'd':
                self.manage_environment()
            elif choice == 'e':
                self.change_process_priority()
            elif choice == 'f':
                self.show_system_info()
            elif choice == 'g':
                print("Программа завершена")
                self.running = False
            else:
                print("Неверный выбор. Пожалуйста, выберите a-g")
                wait_for_enter()
