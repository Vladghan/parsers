from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
import random
import lxml
from stdiomask import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

header = {
    "accept-ranges": "bytes",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
}

followers = 1  # индекс числа подписчиков
following = 2  # индекс числа подписок пользователя


# Авторизация
def authorize(driver):
    username = input('Введите логин: ')
    # password = getpass(prompt='Введите пароль: ', mask='*')
    password = input('Введите пароль: ')
    driver.implicitly_wait(8)
    driver.get('https://www.instagram.com')
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.execute_script("document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[0].click()")
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sqdOP.L3NKy.y3zKF')))
    driver.execute_script("document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[0].click()")
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.aOOlW.HoLwm')))
    driver.execute_script("document.getElementsByClassName('aOOlW   HoLwm ')[0].click()")


# Получение списка подписчиков и подписок
def get_follow(driver, index=None):
    driver.implicitly_wait(1)
    if index not in (1, 2):
        return "index должен равняться 1 (подписчики) или 2 (на кого ты подписан)"
    driver.get('https://www.instagram.com/the_vladcha')
    followers_number = int(bs(driver.page_source, 'lxml').find_all(class_='g47SY')[index].string)
    driver.execute_script(f"document.getElementsByClassName('-nal3 ')[{index}].click()")
    folls = []
    element = driver.find_elements_by_class_name('isgrP')[-1]
    while len(folls) < followers_number:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        content = bs(driver.page_source, 'lxml')
        folls = content.find_all(class_='FPmhX')
    followers_list = [i.get('title') for i in folls]
    return followers_list


# Число новых сообщений
def messages_count(driver):
    driver.get('https://www.instagram.com/direct/inbox/')
    time.sleep(2)
    inbox = bs(driver.page_source, 'lxml')
    try:
        queries_text = inbox.find_all('h5')[0].text
    except Exception:
        queries_text = None
    driver.get('https://www.instagram.com')
    time.sleep(2)
    content = bs(driver.page_source, 'lxml')
    try:
        messages_count = int(content.find_all('div', attrs={'class': 'KdEwV'})[0].text)
    except Exception:
        messages_count = 0
    return queries_text, messages_count


# Число непросмотренных сторис
def get_stories_count(driver):
    stories_divs = []
    scroll = True
    while scroll:
        try:
            content = bs(driver.page_source, 'lxml')
            stories_divs.extend(content.find_all('div', attrs={'class': 'eebAO h_uhZ'}))
            driver.execute_script("document.getElementsByClassName('  _6CZji oevZr  ')[0].click()")
            time.sleep(1)
        except Exception as E:
            scroll = False
    return len(set(stories_divs))


# Просмотр сторис
def watch_stories(driver):
    watching = True
    counter = 0
    limit = random.randint(5, 45)
    driver.execute_script("document.getElementsByClassName('OE3OK ')[0].click()")
    try:
        while watching:
            time.sleep(random.randint(10, 15))
            if random.randint(1, 5) == 5:
                driver.execute_script("document.getElementsByClassName('FhutL')[0].click()")
            counter += 1
            if counter > limit:
                driver.execute_script("document.getElementsByClassName('wpO6b ')[1].click()")
                watching = False
    except Exception as E:
        print(E)
        watching = False


# Просмотр страницы с постами
def scroll_feed(driver):
    scrolling = True
    last_height = driver.execute_script("return document.body.scrollHeight")
    while scrolling:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(4, 10))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or random.randint(1, 10) == 1:
            scrolling = False
        last_height = new_height


# Просмотр страницы с рекомендациями
def scroll_recomendations(driver):
    driver.get('https://www.instagram.com/explore/people/suggested/')
    time.sleep(5)
    scrolling = True
    last_height = driver.execute_script("return document.body.scrollHeight")
    while scrolling:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(4, 10))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or random.randint(1, 10) == 1:
            scrolling = False
        last_height = new_height
        if random.randint(0, 1):
            try:
                driver.execute_script(
                    f"document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[{random.randint(1, 100)}].click()")
            except Exception as E:
                print(E)


def scroll_explore(driver):
    driver.get('https://www.instagram.com/explore')
    time.sleep(3)
    scrolling = True
    last_height = driver.execute_script("return document.body.scrollHeight")
    while scrolling:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(4, 10))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or random.randint(1, 5) == 1:
            scrolling = False
        last_height = new_height


driver = webdriver.Chrome(ChromeDriverManager().install())
# Вызов необходимых функций
authorize(driver)
# queries_text, messages_count = messages_count(driver)
# stories_count = get_stories_count(driver)
followers = get_follow(driver, index=followers)
following = get_follow(driver, index=following)
# watch_stories(driver)
# scroll_recomendations(driver)
# scroll_feed(driver)
# scroll_explore(driver)
driver.quit()

# if queries_text is not None:
#     print(queries_text)
# else:
#     print('Нет новых запросов на диалог')
# print('Новых сообщений:', messages_count)

# print('Новых историй:', stories_count)

super_users = ['coco_nady', 'p_photogram8', 'nikitadeft', 'illiahlad', 'valentin_hris', 'vitwai', 'balena_hair',
               'brandonwoelfel', 'mrfreemax', 'polyaizderevki', 'spoontamer']
rats = []
print('Список предателей:')
# Вычисление людей, не подписанных на меня ;)
for item in following:
    if item not in followers and item not in super_users:
        rats.append(item)
        print(item)
