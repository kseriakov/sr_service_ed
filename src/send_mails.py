from pathlib import Path
import sys, os
import django
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model


_new_route = Path.cwd()
# Добавляем в пути для поиска модулей питона текущую директорию
sys.path.append(_new_route)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sc_service.settings'
django.setup()
from scraping.models import *


qs = get_user_model().objects.filter(send_mail=True).values('city', 'language', 'email')
user_dict = {}
for item in qs:
    user_dict.setdefault((item['city'], item['language']), [])
    user_dict[(item['city'], item['language'])].append(item['email'])

if user_dict:
    conditions = {'city_id__in': [], 'language_id__in': []}
    for key in user_dict.keys():
        conditions['city_id__in'].append(key[0])
        conditions['language_id__in'].append(key[1])

    vacancy_for_send = Vacancy.objects.filter(**conditions)[:10].values()
    content_for_send = {}
    for vacancy in vacancy_for_send:
        content_for_send.setdefault((vacancy['city_id'], vacancy['language_id']), [])
        content_for_send[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)

    for k, v in user_dict.items():
        content = content_for_send.get(k, [])
        html = ''
        for item in content:
            html += f'<a href="{ item["url"] }">{ item["title"] }</a>'
            html += f'<p>{ item["description"] }</p>'
            html += f'<p>{ item["company"] }</p><br><hr>'

html = html


subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
text_content = 'This is an important message.'
html_content = '<p>This is an <strong>important</strong> message.</p>'
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")
msg.send()
