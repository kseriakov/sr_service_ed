import asyncio
import json
from pathlib import Path
import sys, os


# ЗАПУСК ДЖАНГО ИЗ ДРУГОЙ ПАПКИ, НЕ В ПРОЕКТЕ
from django.contrib.auth import get_user_model
from django.db import DatabaseError

_new_route = Path.cwd()
# Добавляем в пути для поиска модулей питона текущую директорию
sys.path.append(_new_route)

# Теперь импортируем джанго
import django
# Добавляем в переменные окружения путь с настройками нашего проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'sc_service.settings'
django.setup()

# Теперь можно делать импорт модулей
from scraping.models import *
from scraping.parcers import *


def get_unique_city_lang():
    user = get_user_model()
    qs = user.objects.filter(send_mail=True).values('city_id', 'language_id')
    res = set((i['city_id'], i['language_id']) for i in qs)
    return res


def get_urls(set_city_lang):
    qs = Url.objects.all().values()
    urls_dict = {(i['city_id'], i['language_id']): i['data'] for i in qs}
    urls = []
    for pair in set_city_lang:
        d = {
            'city_id': pair[0],
            'language_id': pair[1],
            'data': urls_dict.get(pair)
        }
        urls.append(d)

    return urls


set_unique_city_lang = get_unique_city_lang()
set_urls = get_urls(set_unique_city_lang)

parsers = (
    (hh_ru, 'hh_ru'),
    (super_job, 'super_job'),
)

jobs, errors = [], []


# ИСПОЛЬЗУЕМ АСИНХРОННОСТЬ
async def main(value):
    func, url, city_id, language_id = value
    job, err = await loop.run_in_executor(None, func, url, city_id, language_id)
    jobs.extend(job)
    errors.extend(err)

# Асинхронное выполнение цикла
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# Создаем список задач на выполнение
tmp_tasks = [
    (func, item['data'][key], item['city_id'], item['language_id'])
    for item in set_urls
    for func, key in parsers
    if item['data']
]
# Создаем задачи
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

loop.run_until_complete(tasks)
loop.close()

# Сделали решение этого цикла асинхронно
# for item in set_urls:
#     for func, key in parsers:
#         if item['data']:
#             j, e = func(item['data'][key], item['city_id'], item['language_id'])
#             jobs += j
#             errors += e
#
for job in jobs:
    try:
        Vacancy.objects.create(**job)
    except DatabaseError:
        pass

# with open('jobs.json', 'w') as j, open('errors.json', 'w') as e:
#     j.write(json.dumps(jobs))
#     e.write(json.dumps(errors))
