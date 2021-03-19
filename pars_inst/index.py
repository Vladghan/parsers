from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
import random
import lxml

header = {
    "accept-ranges": "bytes",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
}


# Авторизация
def authorize(driver):
    username = input()
    password = input()
    driver.get('https://www.instagram.com')
    time.sleep(5)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.execute_script("document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[0].click()")
    time.sleep(10)
    driver.execute_script("document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[0].click()")
    time.sleep(10)
    driver.execute_script("document.getElementsByClassName('aOOlW   HoLwm ')[0].click()")


# Получение списка подписчиков
def get_follower(driver):
    driver.get('https://www.instagram.com/the_vladcha')
    time.sleep(2)
    driver.execute_script("document.getElementsByClassName('-nal3 ')[1].click()")
    time.sleep(1)
    followers_list = []
    scroll = True
    element = driver.find_elements_by_class_name('isgrP')[-1]
    while scroll:
        last_height = driver.find_elements_by_class_name('FPmhX')[-1]

        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        time.sleep(2)
        new_height = driver.find_elements_by_class_name('FPmhX')[-1]
        if new_height == last_height:
            scroll = False
    content = bs(driver.page_source, 'lxml')
    folls = content.find_all(class_='FPmhX')
    for foll in folls:
        followers_list.append(foll.get('title'))
    return followers_list


# Получение списка, на кого Вы подписаны
def get_following(driver):
    driver.get('https://www.instagram.com/the_vladcha')
    time.sleep(2)
    driver.execute_script("document.getElementsByClassName('-nal3 ')[2].click()")
    time.sleep(1)
    following_list = []
    scroll = True
    element = driver.find_elements_by_class_name('isgrP')[-1]
    while scroll:
        last_height = driver.find_elements_by_class_name('FPmhX')[-1]

        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        time.sleep(2)
        new_height = driver.find_elements_by_class_name('FPmhX')[-1]
        if new_height == last_height:
            scroll = False
    content = bs(driver.page_source, 'lxml')
    folls = content.find_all(class_='FPmhX')
    for foll in folls:
        following_list.append(foll.get('title'))
    return following_list


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
followers = get_follower(driver)
following = get_following(driver)
# watch_stories(driver)
# scroll_recomendations(driver)
# scroll_feed(driver)
# scroll_explore(driver)

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
