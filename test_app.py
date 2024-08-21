import unittest
from wsgiref.util import setup_testing_defaults
from app import application
import json
import io

class TestApp(unittest.TestCase):

    # Метод для создания и отправки mock-запросов к приложению
    def mock_request(self, method, path, body=None):
        environ = {}
        setup_testing_defaults(environ)  # Установка стандартных значений для окружения WSGI
        environ['REQUEST_METHOD'] = method  # Установка метода запроса (GET или POST)
        environ['PATH_INFO'] = path  # Установка пути запроса
        if body:
            environ['CONTENT_LENGTH'] = str(len(body))  # Установка длины тела запроса
            environ['wsgi.input'] = io.BytesIO(body.encode('utf-8'))  # Установка тела запроса
        else:
            environ['CONTENT_LENGTH'] = '0'
            environ['wsgi.input'] = io.BytesIO(b'')

        response_body = []
        status = []
        headers = []

        # Функция для сохранения статуса и заголовков ответа
        def start_response(s, h):
            status.append(s)
            headers.extend(h)

        # Вызов основного приложения с mock-окружением
        result = application(environ, start_response)
        response_body = b''.join(result).decode('utf-8')  # Сборка тела ответа

        return status[0], headers, response_body

    # Тест для проверки получения текущего времени в GMT
    def test_get_gmt(self):
        status, headers, body = self.mock_request('GET', '/')
        self.assertEqual(status, '200 OK')
        self.assertIn('Current time in GMT:', body)

    # Тест для проверки получения текущего времени в другой временной зоне
    def test_get_timezone(self):
        status, headers, body = self.mock_request('GET', '/Europe/Moscow')
        self.assertEqual(status, '200 OK')
        self.assertIn('Current time in Europe/Moscow:', body)

    # Тест для проверки конвертации времени из одной временной зоны в другую
    def test_convert_timezone(self):
        body = json.dumps({
            "date": {"date": "12.20.2021 22:21:05", "tz": "EST"},
            "target_tz": "Europe/Moscow"
        })
        status, headers, body = self.mock_request('POST', '/api/v1/convert', body)
        self.assertEqual(status, '200 OK')
        data = json.loads(body)
        self.assertIn('converted_date', data)

    # Тест для проверки вычисления разницы во времени между двумя датами в разных временных зонах
    def test_date_diff(self):
        body = json.dumps({
            "first_date": "12.06.2024 22:21:05", "first_tz": "EST",
            "second_date": "12:30pm 2024-02-01", "second_tz": "Europe/Moscow"
        })
        status, headers, body = self.mock_request('POST', '/api/v1/datediff', body)
        self.assertEqual(status, '200 OK')
        data = json.loads(body)
        self.assertIn('difference_seconds', data)

# Запуск всех тестов
if __name__ == '__main__':
    unittest.main()  
