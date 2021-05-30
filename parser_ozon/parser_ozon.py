"""Парсер из Django приложения"""

import os
import re
import time

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import lxml
from random import randint
from trainees_three.settings import BROWSER_ACCEPT, BROWSER_USER_AGENT
import csv
import undetected_chromedriver.v2 as uc

driver = uc.Chrome()


# Декоратор-счетчик
def counter(func):
    print("Начинаем")

    def wrapper(self, *args, **kwargs):
        wrapper.count += 1
        rez = func(self, *args, **kwargs)
        print(f"# Итерация {wrapper.count} записана...")
        return rez

    wrapper.count = 0
    return wrapper


# '.b6q0' - ничего не найдено
# '.b6k2' - блок товаров
# '.a0c4' - сам товар
# '.a0f2' - названия товаров
# '.b5v6' - настоящая цена

class ParserOzon:

    def __init__(self):
        self.url = 'https://www.ozon.ru/search/?from_global=true&text='
        self.headers = {
            "Accept": BROWSER_ACCEPT,
            "User-Agent": BROWSER_USER_AGENT,
        }

    def parser(self, url):
        with driver:
            driver.get(url)
            # req = requests.get(url, self.headers)
            # src = req.text
            driver.implicitly_wait(5)
            time.sleep(randint(3, 6))
            src = driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            return soup

    # Создание csv файла с заголовками
    def create_file(self):
        if not os.path.exists('data_ozon.csv'):
            with open('data_ozon.csv', 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(('Товар',
                                 'Цена',))

    # Парсинг продуктов
    def get_products(self, number):
        self.create_file()
        with open("запросы к озону.txt", encoding='utf-8') as file:
            for i in range(number):
                data = file.readline().strip().replace(" ", "+")
                page = 1
                count = 0
                while True:
                    soup = self.parser(self.url + data + f"&page={page}")
                    if soup.find_all('div', class_='b6q0'):
                        print("Страница не найдена")
                        break

                    block_products = soup.find('div', class_='b6k2')
                    all_products = block_products.find_all('div', class_='a0c4')
                    for product in all_products:
                        self.save_data(product)
                        count += 1

                    # Проверка наличия кнопки "Дальше" в пагиниции
                    if not soup.find('div', class_='b9i0'):
                        break
                    page += 1
                    print("Страница записана...")
                print(f"Категория №{i + 1} - '{data}' записана...")
                print(f'Записано товаров: {count}')

    # Сохранение данных продуктов
    @counter
    def save_data(self, product):
        with open('data_ozon.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)

            title = product.find('span', class_='a0f2').string.strip()
            while "  " in title:
                title = title.replace('  ', ' ')
            price_str = product.find('span', class_='b5v6').string
            price = re.sub(r"[ ₽ ]", "", price_str)

            writer.writerow((title, price))


class Command(BaseCommand):
    help = 'Парсинг citilink'

    def handle(self, *args, **options):
        p = ParserOzon()
        p.get_products(int(input("Введите число категорий (МАКС. - 163): ")))
