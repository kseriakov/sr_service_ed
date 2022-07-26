import requests
from bs4 import BeautifulSoup as bs
import json
from random_user_agent.user_agent import UserAgent


__all__ = ('work', 'hh_ru', 'super_job')

user_agent_rotator = UserAgent()
random_user_agent = user_agent_rotator.get_random_user_agent()

headers = {
    'User-Agent': random_user_agent,
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8', }


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


def hh_ru(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        request = requests.get(url=url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser')
            div_main = soup.find('div', attrs={'id': 'a11y-main-content'})
            if div_main:
                div_list = div_main.find_all('div', class_='serp-item')
                for item in div_list:
                    title = item.find('a').string
                    href = item.find('a')['href']
                    company = 'Noname'
                    try:
                        company = item.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    except:
                        pass
                    try:
                        content = item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).string +'\n'
                    except:
                        content = ''
                    try:
                        if content_req := item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}):
                            content += content_req.string
                    except:
                        content = content or 'No content'

                    jobs.append({'title': title, 'url': href, 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def super_job(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://russia.superjob.ru'
    if url:
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
                        # Получение атрибута тега img
                        company = cmp.img['alt']
                    content_list = item.find_all('span')
                    for i in content_list:
                        if len(i.text) > 70:
                            content = i.text
                            break
                    else:
                       content = 'No content'

                    jobs.append({'title': title, 'url': href, 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://russia.superjob.ru/vacancy/search/?keywords=python'
    jobs, errors = hh_ru(url)
    with open('jobs.json', 'w') as j, open('errors.json', 'w') as e:
        j.write(json.dumps(jobs))
        e.write(json.dumps(errors))
