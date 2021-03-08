# Парсинг самых рейтинговых фильмов с сайта ivi.ru и сохранение данных в csv-файл

import csv
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import os
from slugify import slugify

# Создание csv файла с заголовками
with open('movies.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(('Фильмы',
                     'Дата',
                     'Жанр',
                     'Страна',
                     'В главной роли',
                     'Режиссер',
                     'Рейтинг на ivi',
                     'poster'))

url = "https://www.ivi.ru/rating"
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
}

items = 9
print("Начинаем")
count = 0


for item in range(8, items):
    url = f"https://www.ivi.ru/rating/page{item}?rating_part=main"

    req = requests.get(url=url, headers=headers)
    src = req.text

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(src)

    with open('index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all_films = soup.find('ul', class_='gallery_adaptive').find_all('a', class_='item-content-wrapper')

    for film in all_films:
        title = film.find('img').get('alt')
        link = 'https://www.ivi.ru' + film.get('href')
        req = requests.get(link, headers)
        src = req.text
        copy_page = f"{slugify(title)}.html"
        with open(copy_page, 'w', encoding='utf-8') as file:
            file.write(src)

        with open(copy_page, encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        persons = soup('div', class_='fixedSlimPosterBlock__textSection', limit=4)

        director = ''
        actors = []
        for person in persons:
            try:
                somebody = person.find(class_='fixedSlimPosterBlock__title').string + ' ' + person.find(
                    class_='fixedSlimPosterBlock__secondTitle').string
            except AttributeError:
                somebody = person.find(class_='fixedSlimPosterBlock__title').string
            if person == persons[0]:
                director = somebody
            else:
                actors.append(somebody)

        parameters_info = [i for i in soup.find(class_='parameters__info').strings if i != ', ']

        year = parameters_info[0]
        country = parameters_info[1]
        genres = parameters_info[2:]
        genre = []
        for i in genres:
            genre.append(i.string)

        rating = soup.find(class_='nbl-ratingAmple__valueInteger').text + soup.find(
            class_='nbl-ratingAmple__valueFraction').text
        poster = soup.find('video-info').get('data-poster')

        with open('movies.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow((title,
                             year,
                             genre,
                             country,
                             actors,
                             director,
                             rating,
                             poster))

        count += 1
        print(f"# Итерация {count} записана...")

        sleep(random.randrange(1, 3))
        os.remove(copy_page)
    os.remove('index.html')
print('Конец')

# top_info = soup.find('div', class_='topInfo__grid')
