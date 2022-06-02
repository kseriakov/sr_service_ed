import requests
from bs4 import BeautifulSoup as bs
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8', }

url = 'https://www.work.ua/ru/jobs-python/'


def work(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua/'
    request = requests.get(url=url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        div_main = soup.find('div', attrs={'id': 'pjax-job-list'})
        if div_main:
            div_list = div_main.find_all('div', class_='job-link')
            for item in div_list:
                title = item.h2.a.string
                href = domain + item.h2.a['href']
                company = 'Noname'
                if cmp := item.img:
                    company = cmp['alt']
                content = item.p.text

                jobs.append({'title': title, 'url': href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def hh_ru(url):
    jobs = []
    errors = []
    request = requests.get(url=url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        div_main = soup.find('div', attrs={'id': 'a11y-main-content'})
        if div_main:
            div_list = div_main.find_all('div', class_='vacancy-serp-item')
            for item in div_list:
                title = item.find('a').string
                href = item.find('a')['href']
                company = 'Noname'
                if cmp := item.find('img'):
                    company = cmp['alt']
                content = item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).string +'\n'
                if content_req := item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}):
                    content += content_req.string

                jobs.append({'title': title, 'url': href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def super_job(url):
    jobs = []
    errors = []
    domain = 'https://russia.superjob.ru'
    request = requests.get(url=url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        div_list = soup.find_all('div', attrs={'class': 'f-test-vacancy-item'})
        if div_list:
            for item in div_list:
                title = item.find('a').text
                href = domain + item.find('a')['href']
                company = 'Noname'
                if cmp := item.find_all('a').pop(1):
                    company = cmp.string
                content = item.find_all('span')[10].text

                jobs.append({'title': title, 'url': href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://russia.superjob.ru/vacancy/search/?keywords=python'
    jobs, errors = super_job(url)
with open('jobs.json', 'w') as j, open('errors.json', 'w') as e:
    j.write(json.dumps(jobs))
    e.write(json.dumps(errors))

with open('jobs.json', encoding='UTF-8') as f:
    res = json.loads(f.read())
