# server-api-base-pytz

Разработать wsgi приложение (веб приложение использующее интерфейс wsgi для ответа клиенту) реализующее аналог сервиса time.is и предоставляющее работу с временными зонами на базе библиотеки tz
1) по запросу GET /<tz name> отдает текущее время в запрошенной зоне в формате html. <tz name> может быть пустым - тогда в GMT
2) по запросу POST /api/v1/convert - преобразует дату/время из одного часового пояса в другой
принимает: параметр date - json формата {"date":"12.20.2021 22:21:05", "tz": "EST"}  и target_tz - строку с определением зоны
3) по запросу POST /api/v1/datediff- отдает число секунд между между двумя датами из параметра data (json формат {"first_date":"12.06.2024 22:21:05", "first_tz": "EST", "second_date":"12:30pm 2024-02-01", "second_tz": "Europe/Moscow"})

Ограничения:

1) Запрещено использовать веб-фреймворки

2) Для тестирования(запуска) можно использовать как wsgiref, так и сторонние сервера (gunicorn, uwsgi)

3) Код лабораторной должен представлять из себя один (!) файл веб-приложения и один файл теста

4) Выбирая между читаемостью кода и размером - следует соблюдать баланс. Комментарии нужны только там, где это особенно нужно. Имена переменных должны быть понятными.

5) Решение должно быть уникально и авторским

6) К решению должна прилагаться ссылка на проект postman (или аналогичный) с публично доступными тестами всех апи

# тесты в постмане 
https://www.postman.com/dvs67/workspace/pytz-based-api-server/collection/37822531-ba77f79d-19b9-473a-ba94-15e00f889f42
