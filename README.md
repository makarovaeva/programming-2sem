# Programming Course — Laboratory Works

Read this in other languages: [Русский](README_RU.md)

**Author:** Eva Makarova  
**Programming Language:** Python 3  
**Operating System:** Windows  

---

## Table of Contents
1. [Laboratory Work 1. Decorators and Asynchronous Programming](#laboratory-work-1-decorators-and-asynchronous-programming)
2. [Laboratory Work 2. Asynchrony and Multithreading](#laboratory-work-2-asynchrony-and-multithreading)
3. [Laboratory Work 3. Working with the os Library](#laboratory-work-3-working-with-the-os-library)
4. [Laboratory Work 4. Introduction to ORM & SQLAlchemy](#laboratory-work-4-introduction-to-orm--sqlalchemy)
5. [Tests](tests)

---

## Laboratory Work 1. Decorators and Asynchronous Programming

### Tasks:
* **Task 1 — Parameterless Decorator (`logger`):**
  Implementation of a `logger` decorator that outputs the function name, its arguments, return value, and execution time.
* **Task 2 — Parameterized Decorator (`retry`):**
  Implementation of a `retry(attempts, delay, exceptions=None)` decorator that retries function execution upon encountering errors specified in `exceptions` for a given number of `attempts` with a delay of `delay` seconds.
* **Task 3 — Parameterless Class Decorator (`logger`):**
  A class decorator that logs the class name, methods (including magic methods), arguments, and execution time. Added a `show_magic_methods` flag to toggle logging of magic methods.
* **Task 4 — Parameterized Class Decorator (`call_limiter`):**
  Implementation of a `call_limiter(limit)` decorator that restricts the number of invocations for each class method to `limit` times.
* **Task 5 — Introduction to Asynchrony:**
  Implementation of two asynchronous functions with `asyncio.sleep()` intervals to demonstrate non-blocking execution.

---

## Laboratory Work 2. Asynchrony and Multithreading

### Tasks:
* **Task 1 — Basic Asynchronous Functions:**
  An asynchronous function that waits for `delay` seconds and outputs a `message`.
* **Task 2 — Concurrent Execution with `asyncio.gather`:**
  Execution of three concurrent tasks with different delays (2, 1, and 3 seconds) and distinct text outputs.
* **Task 3 — Synchronous vs. Asynchronous API Requests:**
  Performance comparison between sequential HTTP requests via `requests` and asynchronous requests using `aiohttp` to external web resources. Execution time measurement and response ordering analysis.
* **Task 4 — Working with Threads (`threading`):**
  Comparison between sequential function calls with a delay and its parallel execution across 3 separate threads.
* **Task 5 — Data Race Condition:**
  Demonstration of a race condition during improper concurrent increments of a shared global variable from multiple threads.
* **Task 6 — Resolving the Data Race Condition:**
  Application of the `threading.Lock` synchronization primitive to protect the critical section and prevent data races.

---

## Laboratory Work 3. Working with the os Library

**Objective:** Exploring systemic capabilities of the `os` library without using external command shells (`cmd`, `bash`).

### Tasks:
* **Task 1 — File Operations Script:**
  * Validating and adjusting the current working directory.
  * Creating a file, writing data, and verifying existence via `os.path`.
  * Retrieving file size, last access time, and modification time.
  * Fetching the system's current username.
  * Reading and modifying file access permissions (`os.chmod`).
* **Task 2 — Directory Operations Script:**
  * Copying, renaming, and moving files across nested directories using `os` methods.
  * Moving and renaming a file in a single operation.
  * Recursive traversal and display of directory trees and files (`os.walk`).
  * Creating and removing temporary and nested folders.
* **Task 3 — System Management Script (Interactive Manager):**
  A console-based interactive menu providing the following functionality:
  * `a)` List of all running processes;
  * `b)` Detailed information about a specific process;
  * `c)` Process termination by PID;
  * `d)` Viewing and updating environment variables (`os.environ`);
  * `e)` Modifying process priority;
  * `f)` Displaying system information;
  * `g)` Exit.
  * *Exception handling for missing permissions (`PermissionError`).*

---

## Laboratory Work 4. Introduction to ORM & SQLAlchemy

**Objective:** Using SQLAlchemy ORM to design data models, relationships, and execute CRUD operations for a basic book reservation system.

### Entities and DB Schema:
* **User:** `id` (PK), `name` (Not Null), `email` (Unique, Not Null).
* **Book:** `id` (PK), `title` (Not Null), `author` (Not Null), `copies_available` (Integer).
* **Booking:** `id` (PK), `user_id` (FK → User.id), `book_id` (FK → Book.id), `booking_date` (Date).

### Implemented Features:
1. Setting up SQLite / PostgreSQL connections inside a Docker container.
2. Database table creation via `Base.metadata.create_all()`.
3. Inserting new users and books into the database.
4. Creating a booking with an automatic reduction of `copies_available`.
5. Canceling/deleting a booking with a corresponding increase in available copies.