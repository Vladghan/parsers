# Парсинг самых рейтинговых фильмов с сайта ivi.ru с помощью класса и сохранение данных в csv-файл

import csv
import random
from time import sleep
import requests
from bs4 import BeautifulSoup


# Декоратор-счетчик
def counter(func):
    print("Начинаем")

    def wrapper(self, *args, **kwargs):
        wrapper.count += 1
        rez = func(self, *args, **kwargs)
        print(f"# Итерация {wrapper.count} записана...")
        sleep(random.randrange(2, 4))
        return rez

    wrapper.count = 0
    return wrapper


# Декоратор для создания и сохранения данных в таблицу в csv файл
def csv_save(func):
    with open('movies.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Фильмы',
                         'Категория',
                         'Дата',
                         'Жанр',
                         'Страна',
                         'В главной роли',
                         'Режиссер',
                         'Рейтинг на ivi',
                         'Постер'))

    def wrapper(self, *args, **kwargs):
        rez = func(self, *args, **kwargs)
        with open('movies.csv', 'a', encoding='utf-8', newline='') as wrapper.file:
            wrapper.writer = csv.writer(wrapper.file)
            wrapper.writer.writerow((rez['Фильмы'],
                                     rez['Категория'],
                                     rez['Дата'],
                                     rez['Жанр'],
                                     rez['Страна'],
                                     rez['В главной роли'],
                                     rez['Режиссер'],
                                     rez['Рейтинг на ivi'],
                                     rez['poster']))
        return rez

    return wrapper


class ParserIvi:

    def __init__(self):
        self.url = 'https://www.ivi.ru'
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        }

    # Парсинг страницы со списком фильмов
    def parser_page(self):
        item = 0
        while True:
            url = self.url + f"/rating/page{item}?rating_part=main"
            item += 1
            req = requests.get(url, self.headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')

            # Проверка наличия страницы
            top_info = soup.find('div', class_='topInfo__grid')
            if top_info is not None:
                print('Страница не найдена')
                break

            all_films = soup.find('ul', class_='gallery_adaptive').find_all('a', class_='item-content-wrapper')
            for film in all_films:
                title = film.find('img').get('alt')
                link = self.url + film.get('href')
                self.parser_block(link, title)
                # Генератор, останавливает работу скрипта после вывода десяти фильмов и начинает следующ
                if (all_films.index(film) + 1) % 10 == 0:
                    yield

    # Парсинг страницы одного фильма
    @counter
    @csv_save
    def parser_block(self, link, title):
        req = requests.get(link, self.headers)
        src = req.text
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

        category = soup.find('ul', class_='headerBar__breadCrumbs').contents[1].find('span').string

        parameters_dict = {'Фильмы': title,
                           'Категория': category,
                           'Дата': year,
                           'Жанр': genre,
                           'Страна': country,
                           'В главной роли': actors,
                           'Режиссер': director,
                           'Рейтинг на ivi': rating,
                           'poster': poster}

        return parameters_dict


def main():
    p = ParserIvi()
    next(p.parser_page())
    print('Конец сета...')


if __name__ == '__main__':
    main()
