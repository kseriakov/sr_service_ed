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
if errors_data:
    html_err = ''
    for item in errors_data.first().data:
        html_err += f'<a href="{ item["url"] }">Errors: { item["title"] }</a><br><hr>'

    msg = EmailMultiAlternatives(f'Ошибки скрапинга на {to_day}', 'Ошибки скрапинга', from_email, to=(EMAIL_ADMIN_USER, ))
    msg.attach_alternative(html_err, "text/html")
    msg.send()


all_users = get_user_model().objects.all().values('city', 'language')

all_set_city_lang = {(i['city'], i['language']) for i in all_users}

no_urls = ''
for item in list(all_set_city_lang):
    if item not in user_dict:
        no_urls += f'<h6>Отсутствует url для пары - город: {item[0]}, язык: {item[1]}</h6><br><hr>'

if no_urls:
    msg = EmailMultiAlternatives(f'Обнаружены недостающие urls', 'Надо добавить urls', from_email, to=(EMAIL_ADMIN_USER, ))
    msg.attach_alternative(no_urls, "text/html")
    msg.send()
