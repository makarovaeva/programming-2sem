import asyncio
import logging
import time

import aiohttp
import requests
from requests import HTTPError, RequestException

from lab2.time_decorator import time_decorator


class HttpClient:
    """
    HTTP-клиент для выполнения синхронных и асинхронных запросов к списку URL.

    Класс предоставляет функциональность для измерения времени ответа от
    веб-серверов как в синхронном (последовательном), так и в асинхронном
    (конкурентном) режимах. Результаты запросов сохраняются и могут быть
    отсортированы для анализа.

    Attributes:
        _urls (list[str]): Список URL-адресов для выполнения запросов
        _sync_result (list[tuple[float, str]]): Результаты синхронных запросов
        _async_result (list[tuple[float, str]]): Результаты асинхронных запросов
    """

    def __init__(self, urls: list[str]) -> None:
        """
        Инициализирует HTTP-клиент со списком URL для тестирования.

        Args:
            urls (list[str]): Список URL-адресов для выполнения запросов
        """
        self._urls = urls
        self._sync_result = []
        self._async_result = []

    def get_urls(self) -> list[str]:
        """
        Возвращает список URL-адресов, используемых клиентом.

        Returns:
            list[str]: Список URL-адресов для выполнения запросов
        """
        return self._urls

    def get_sync_res(self) -> list[tuple[float, str]]:
        """
        Возвращает результаты синхронных запросов.

        Returns:
            list[tuple[float, str]]: Список кортежей (время ответа, URL)
        """
        return self._sync_result

    def get_async_res(self) -> list[tuple[float, str]]:
        """
        Возвращает результаты асинхронных запросов.

        Returns:
            list[tuple[float, str]]: Список кортежей (время ответа, URL)
        """
        return self._async_result

    @time_decorator
    def _get_sync_responses(self) -> None:
        """
        Внутренний метод для последовательного выполнения HTTP-запросов.

        Выполняет GET-запросы к каждому URL из списка последовательно,
        измеряет время ответа и сохраняет результаты в _sync_result.
        В случае ошибки запроса выводит сообщение об исключении.

        Декорирован time_decorator для измерения общего времени выполнения.

        Returns:
            None
        """
        for url in self.get_urls():
            try:
                t = _get_sync(url)
                self.get_sync_res().append((t, url))
            except (RequestException, HTTPError) as e:
                print(e)

    def print_sync_responses(self) -> float:
        """
        Выполняет синхронные запросы и выводит отсортированные результаты.

        Запускает последовательное выполнение запросов через _get_sync_responses,
        сортирует результаты по времени ответа и выводит их на экран.

        Returns:
            float: Общее время выполнения всех синхронных запросов
        """
        t, _ = self._get_sync_responses()
        self.get_sync_res().sort()
        for time, url in self.get_sync_res():
            print(f"Запрос к сайту {url} составил {time:.2f} сек")
        return t

    @time_decorator
    async def _get_async_responses(self) -> None:
        """
        Внутренний метод для конкурентного выполнения HTTP-запросов.

        Создает задачи для каждого URL и выполняет их конкурентно через
        asyncio.gather, измеряет время ответа для каждого запроса и
        сохраняет результаты в _async_result. В случае ошибки запроса
        выводит сообщение об исключении.

        Декорирован time_decorator для измерения общего времени выполнения.

        Returns:
            None
        """
        tasks = [_get_async(path) for path in self.get_urls()]

        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            url = self.get_urls()[i]

            if isinstance(result, Exception):
                error_type = type(result).__name__
                logger.error(f"Ошибка для {url}: {error_type} - {result}")
            else:
                self.get_async_res().append((result, url))

    async def print_async_responses(self) -> float:
        """
        Выполняет асинхронные запросы и выводит отсортированные результаты.

        Запускает конкурентное выполнение запросов через _get_async_responses,
        сортирует результаты по времени ответа и выводит их на экран.

        Returns:
            float: Общее время выполнения всех асинхронных запросов
        """
        t, _ = await self._get_async_responses()
        self.get_async_res().sort()
        for time, url in self.get_async_res():
            print(f"Запрос к сайту {url} составил {time:.2f} сек")
        return t


def _get_sync(path: str) -> float:
    """
    Выполняет HTTP GET-запрос и возвращает время ответа.

    Внутренняя функция для выполнения одиночного HTTP-запроса и измерения
    времени получения ответа. Использует синхронную библиотеку requests.

    Args:
        path (str): URL-адрес для выполнения запроса

    Returns:
        float: Время ответа сервера в секундах

    Raises:
        HTTPError: При возникновении HTTP-ошибки (4xx, 5xx)
        RequestException: При других ошибках запроса (таймаут, соединение и т.д.)
    """
    try:
        response = requests.get(path)
        response.raise_for_status()
        return response.elapsed.total_seconds()
    except HTTPError as e:
        raise HTTPError(f"HTTP ошибка: {e}")
    except RequestException as e:
        raise RequestException(f"Ошибка запроса: {e}")


logger = logging.getLogger(__name__)


async def _get_async(path: str) -> float:
    """
    Асинхронный GET-запрос с измерением времени ответа.

    Args:
        path: URL для запроса

    Returns:
        Время ответа сервера в секундах.

    Raises:
        aiohttp.ClientResponseError: HTTP ошибка (4xx, 5xx).
        aiohttp.ClientConnectionError: Ошибка соединения.
        asyncio.TimeoutError: Превышен таймаут запроса.
        aiohttp.InvalidURL: Некорректный URL.
        Exception: Непредвиденная ошибка.
    """
    try:
        timeout = aiohttp.ClientTimeout(total=30, connect=5)
        response_time = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with session.get(path, timeout=timeout) as response:
                response.raise_for_status()
                await response.read()
                return time.perf_counter() - response_time

    except aiohttp.ClientResponseError as e:
        logger.error(f"HTTP ошибка {e.status} для {path}: {e.message}")
        raise
    except aiohttp.ClientConnectionError as e:
        logger.error(f"Ошибка соединения для {path}: {e}")
        raise
    except asyncio.TimeoutError as e:
        logger.error(f"Таймаут запроса для {path}: {e}")
        raise
    except aiohttp.InvalidURL as e:
        logger.error(f"Некорректный URL {path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка для {path}: {e}")
        raise RuntimeError(f"Ошибка при запросе к {path}: {e}") from e
