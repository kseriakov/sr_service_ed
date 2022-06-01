import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
}

url = 'https://www.work.ua/ru/jobs-python/'
request = requests.get(url=url, headers=headers)
with open('works.html', 'wb') as f:
    f.write(request.content)

