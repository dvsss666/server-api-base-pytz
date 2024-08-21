from wsgiref.simple_server import make_server
import pytz
from datetime import datetime
import json

def application(environ, start_response):
    # Получение пути и метода запроса
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', '')

    # Обработка GET-запроса для получения текущего времени в указанной временной зоне
    if method == 'GET' and (path == '/' or path.startswith('/')):
        tz_name = path[1:] if len(path) > 1 else 'GMT'
        try:
            tz = pytz.timezone(tz_name)  # Получение объекта временной зоны
            current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [f"<html><body><h1>Current time in {tz_name}: {current_time}</h1></body></html>".encode('utf-8')]
        except pytz.UnknownTimeZoneError:  # Обработка ошибки неизвестной временной зоны
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'Timezone not found']

    # Обработка POST-запроса для преобразования времени из одной временной зоны в другую
    elif method == 'POST' and path == '/api/v1/convert':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))  # Получение размера тела запроса
            request_body = environ['wsgi.input'].read(request_body_size)  # Чтение тела запроса
            data = json.loads(request_body)  # Парсинг JSON из тела запроса
            date_str = data['date']['date']
            tz_name = data['date']['tz']
            target_tz_name = data['target_tz']

            source_tz = pytz.timezone(tz_name)  # Исходная временная зона
            target_tz = pytz.timezone(target_tz_name)  # Целевая временная зона
            naive_datetime = datetime.strptime(date_str, '%m.%d.%Y %H:%M:%S')  # Разбор даты без учета временной зоны
            source_datetime = source_tz.localize(naive_datetime)  # Локализация даты в исходной временной зоне
            target_datetime = source_datetime.astimezone(target_tz)  # Преобразование времени в целевую временную зону

            result = target_datetime.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps({'converted_date': result}).encode('utf-8')]
        except (KeyError, ValueError, pytz.UnknownTimeZoneError):  # Обработка ошибок парсинга и некорректных данных
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b'Invalid request']

    # Обработка POST-запроса для вычисления разницы во времени между двумя датами в разных временных зонах
    elif method == 'POST' and path == '/api/v1/datediff':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))  # Получение размера тела запроса
            request_body = environ['wsgi.input'].read(request_body_size)  # Чтение тела запроса
            data = json.loads(request_body)  # Парсинг JSON из тела запроса
            first_date_str = data['first_date']
            first_tz_name = data['first_tz']
            second_date_str = data['second_date']
            second_tz_name = data['second_tz']

            first_tz = pytz.timezone(first_tz_name)  # Первая временная зона
            second_tz = pytz.timezone(second_tz_name)  # Вторая временная зона
            first_naive_datetime = datetime.strptime(first_date_str, '%m.%d.%Y %H:%M:%S')  # Разбор первой даты без учета временной зоны
            second_naive_datetime = datetime.strptime(second_date_str, '%I:%M%p %Y-%m-%d')  # Разбор второй даты без учета временной зоны
            first_datetime = first_tz.localize(first_naive_datetime)  # Локализация первой даты в первой временной зоне
            second_datetime = second_tz.localize(second_naive_datetime)  # Локализация второй даты во второй временной зоне

            diff = int((second_datetime - first_datetime).total_seconds())  # Вычисление разницы в секундах между датами
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps({'difference_seconds': diff}).encode('utf-8')]
        except (KeyError, ValueError, pytz.UnknownTimeZoneError):  # Обработка ошибок парсинга и некорректных данных
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b'Invalid request']

    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

if __name__ == '__main__':
    port = 8051
    httpd = make_server('', port, application)  # Создание и настройка WSGI-сервера
    print(f"Serving on port {port}...")
    httpd.serve_forever()  # Запуск сервера в бесконечном цикле
