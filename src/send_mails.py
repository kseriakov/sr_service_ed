import json
from pathlib import Path
import sys, os
import django
from datetime import date
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model


_new_route = Path.cwd()
# Добавляем в пути для поиска модулей питона текущую директорию
sys.path.append(_new_route)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sc_service.settings'
django.setup()
from scraping.models import *
from sc_service.settings import EMAIL_HOST_USER, EMAIL_ADMIN_USER


to_day = date.today()
empty_content = 'К сожалению по Вашим настройкам вакансий не представлено'
subject = 'Рассылка вакансий'
from_email = EMAIL_HOST_USER
text_content = 'Рассылка вакансий'
admin_email = EMAIL_ADMIN_USER


qs = get_user_model().objects.filter(send_mail=True).values('city', 'language', 'email')
user_dict = {}
for item in qs:
    user_dict.setdefault((item['city'], item['language']), [])
    user_dict[(item['city'], item['language'])].append(item['email'])

if user_dict:
    conditions = {'city_id__in': [], 'language_id__in': []}
    for key in user_dict.keys():
        if key[0] and key[1]:
            conditions['city_id__in'].append(key[0])
            conditions['language_id__in'].append(key[1])

    vacancy_for_send = Vacancy.objects.filter(**conditions, timestamp=to_day).values()
    content_for_send = {}
    for vacancy in vacancy_for_send:
        content_for_send.setdefault((vacancy['city_id'], vacancy['language_id']), [])
        content_for_send[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)

    for k, emails in user_dict.items():
        content = content_for_send.get(k, [])
        html = ''
        for item in content:
            html += f'<a href="{ item["url"] }">{ item["title"] }</a>'
            html += f'<p>{ item["description"] }</p>'
            html += f'<p>{ item["company"] }</p><br><hr>'

        res_html = html if html else empty_content

        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to=(email, ))
            msg.attach_alternative(res_html, "text/html")
            msg.send()


errors_data = Error.objects.filter(timestamp=to_day)
html_err = ''
if errors_data:
    errors_d = errors_data.first()
    if errors_url := errors_d.data.get('errors'):
        html_err += f'<h3>Обнаружены следующие ошибки скрапинга:</h3>'
        for item in errors_url:
            html_err += f'<a href="{ item["url"] }">Errors: { item["title"] }</a><br><hr><br>'

    if user_errors := errors_d.data.get('user_errors'):
        html_err += f'<h3>Необходимо добавить следующие пары: город, ЯП:</h3>'
        for item in user_errors:
            html_err += f'<p>{ item["email"]} --- город: {item["city"]} || ЯП: {item["language"]} </p><br><hr><br>'


all_users = get_user_model().objects.all().values('city', 'language')

all_set_city_lang = {(i['city'], i['language']) for i in all_users}


no_urls = ''
if all_set_city_lang:
    for item in list(all_set_city_lang):
        no_urls += f'<h3>Обнаружены отсутствующие url для следующих пар:</h3>'
        if item not in user_dict:
            no_urls += f'<p>Город: {item[0]}, язык: {item[1]}<p><br><hr>'
    if 'Город' not in no_urls:
        no_urls = ''

if html_err or no_urls:
        msg = EmailMultiAlternatives(subject=f'Системные сообщения', body='В работе сайта обнаружены следующие проблемы',
                                     from_email=from_email, to=(EMAIL_ADMIN_USER,))
        msg.attach_alternative((html_err if html_err else '') + (no_urls if no_urls else ''), "text/html")
        msg.send()



