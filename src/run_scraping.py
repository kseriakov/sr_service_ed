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


def get_unique_lang_city():
    user = get_user_model()
    qs = user.objects.filter(send_mail=True).values('city_id', 'language_id')
    res = set((i['city_id'], i['language_id']) for i in qs)
    return res


print(get_unique_lang_city())

parsers = (
    (hh_ru, 'https://krasnoyarsk.hh.ru/search/vacancy?area=54&text=python'),
    (super_job, 'https://krasnoyarsk.superjob.ru/vacancy/search/?keywords=python'),
)

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

language = Language.objects.get(slug='python')
city = City.objects.get(slug='krasnoyarsk')

for job in jobs:
    try:
        Vacancy.objects.create(**job, language=language, city=city)
    except DatabaseError:
        pass

# with open('jobs.json', 'w') as j, open('errors.json', 'w') as e:
#     j.write(json.dumps(jobs))
#     e.write(json.dumps(errors))
