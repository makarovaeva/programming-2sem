import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import time
import aiohttp
import requests
from requests.exceptions import HTTPError, RequestException

from lab2.task3.http_client import HttpClient, _get_sync, _get_async


class TestHttpClient(unittest.TestCase):
    """
    Тесты для класса HttpClient
    """

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.test_urls = [
            "https://example.com",
            "https://google.com",
            "https://github.com"
        ]
        self.client = HttpClient(self.test_urls)

    def test_initialization(self):
        """
        Тест 1: Проверка инициализации класса
        """
        # Проверяем, что URL сохраняются корректно
        self.assertEqual(self.client.get_urls(), self.test_urls)

        # Проверяем, что результаты инициализируются пустыми списками
        self.assertEqual(self.client.get_sync_res(), [])
        self.assertEqual(self.client.get_async_res(), [])

        # Проверяем, что при пустом списке URL класс создается корректно
        empty_client = HttpClient([])
        self.assertEqual(empty_client.get_urls(), [])

    @patch('lab2.task3.http_client.requests.get')
    def test_get_sync_success(self, mock_get):
        """
        Тест 2: Успешное выполнение синхронного запроса
        """
        # Настраиваем мок для успешного ответа
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_get.return_value = mock_response

        # Вызываем функцию
        result = _get_sync("https://example.com")

        # Проверяем результат
        self.assertEqual(result, 0.5)
        mock_get.assert_called_once_with("https://example.com")
        mock_response.raise_for_status.assert_called_once()

    @patch('lab2.task3.http_client.requests.get')
    def test_get_sync_http_error(self, mock_get):
        """
        Тест 3: Обработка HTTP ошибки в синхронном запросе
        """
        # Настраиваем мок для HTTP ошибки
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        # Проверяем, что выбрасывается исключение
        with self.assertRaises(HTTPError) as context:
            _get_sync("https://example.com")

        self.assertIn("HTTP ошибка", str(context.exception))

    @patch('lab2.task3.http_client._get_sync')
    def test_get_sync_responses_success(self, mock_get_sync):
        """
        Тест 4: Успешное выполнение всех синхронных запросов
        """
        # Настраиваем мок для возврата разных времен ответа
        mock_get_sync.side_effect = [0.1, 0.3, 0.2]

        # Вызываем метод
        self.client._get_sync_responses()

        # Проверяем результаты
        results = self.client.get_sync_res()
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], (0.1, "https://example.com"))
        self.assertEqual(results[1], (0.3, "https://google.com"))
        self.assertEqual(results[2], (0.2, "https://github.com"))

        # Проверяем, что _get_sync вызвана для каждого URL
        self.assertEqual(mock_get_sync.call_count, 3)

    def test_print_sync_responses_sorting(self):
        """
        Тест 5: Проверка сортировки результатов синхронных запросов
        """
        # Заполняем результаты в произвольном порядке
        test_data = [
            (0.5, "https://slow.com"),
            (0.1, "https://fast.com"),
            (0.3, "https://medium.com")
        ]
        for time_val, url in test_data:
            self.client.get_sync_res().append((time_val, url))

        # Сортируем через метод
        with patch('builtins.print') as mock_print:  # Мокаем print чтобы не выводить на экран
            with patch.object(self.client, '_get_sync_responses',
                              return_value=(1.0, None)):  # Мокаем выполнение запросов
                total_time = self.client.print_sync_responses()

        # Проверяем сортировку
        sorted_results = self.client.get_sync_res()
        self.assertEqual(sorted_results[0][0], 0.1)  # fast.com должен быть первым
        self.assertEqual(sorted_results[1][0], 0.3)  # medium.com вторым
        self.assertEqual(sorted_results[2][0], 0.5)  # slow.com третьим


class TestAsyncHttpClient(unittest.IsolatedAsyncioTestCase):
    """
    Асинхронные тесты для HttpClient
    """

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.test_urls = [
            "https://example.com",
            "https://google.com"
        ]
        self.client = HttpClient(self.test_urls)

    async def test_get_async_responses_gather(self):
        """
        Тест 9: Проверка конкурентного выполнения запросов
        """
        # Мокаем _get_async для возврата разных времен
        with patch('lab2.task3.http_client._get_async') as mock_get_async:
            mock_get_async.side_effect = [0.1, 0.2]

            await self.client._get_async_responses()

            # Проверяем результаты
            results = self.client.get_async_res()
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0], (0.1, "https://example.com"))
            self.assertEqual(results[1], (0.2, "https://google.com"))

            # Проверяем, что _get_async вызвана для каждого URL
            self.assertEqual(mock_get_async.call_count, 2)

    async def test_print_async_responses_sorting(self):
        """
        Тест 10: Проверка сортировки асинхронных результатов
        """
        # Заполняем результаты
        test_data = [
            (0.5, "https://slow.com"),
            (0.1, "https://fast.com")
        ]
        for time_val, url in test_data:
            self.client.get_async_res().append((time_val, url))

        # Мокаем _get_async_responses
        with patch('builtins.print') as mock_print:
            with patch.object(self.client, '_get_async_responses', return_value=(0.6, None)):
                total_time = await self.client.print_async_responses()

        # Проверяем сортировку
        sorted_results = self.client.get_async_res()
        self.assertEqual(sorted_results[0][0], 0.1)  # fast.com первый
        self.assertEqual(sorted_results[1][0], 0.5)  # slow.com второй


if __name__ == '__main__':
    unittest.main()
