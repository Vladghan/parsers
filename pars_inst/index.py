from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
import random
import lxml
# import getpass


def authorize(driver):
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    driver.get('https://www.instagram.com')
    time.sleep(5)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.execute_script("document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[0].click()")
    time.sleep(10)
    driver.execute_script("document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[0].click()")
    time.sleep(10)
    driver.execute_script("document.getElementsByClassName('aOOlW   HoLwm ')[0].click()")


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


# def watch_stories(driver):
#     watching = True
#     counter = 0
#     limit = random.randint(5, 45)
#     driver.execute_script("document.getElementsByClassName('OE3OK ')[0].click()")
#     try:
#         while watching:
#             time.sleep(random.randint(10, 15))
#             if random.randint(1, 5) == 5:
#                 driver.execute_script("document.getElementsByClassName('FhutL')[0].click()")
#             counter += 1
#             if counter > limit:
#                 driver.execute_script("document.getElementsByClassName('wpO6b ')[1].click()")
#                 watching = False
#     except Exception as E:
#         print(E)
#         watching = False


# def scroll_feed(driver):
#     scrolling = True
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while scrolling:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.randint(4, 10))
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height or random.randint(1, 10) == 1:
#             scrolling = False
#         last_height = new_height


# def scroll_recomendations(driver):
#     driver.get('https://www.instagram.com/explore/people/suggested/')
#     time.sleep(5)
#     scrolling = True
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while scrolling:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.randint(4, 10))
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height or random.randint(1, 10) == 1:
#             scrolling = False
#         last_height = new_height
#         if random.randint(0, 1):
#             try:
#                 driver.execute_script(
#                     f"document.getElementsByClassName('sqdOP  L3NKy   y3zKF     ')[{random.randint(1, 100)}].click()")
#             except Exception as E:
#                 print(E)


# def scroll_explore(driver):
#     driver.get('https://www.instagram.com/explore')
#     time.sleep(3)
#     scrolling = True
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while scrolling:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.randint(4, 10))
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height or random.randint(1, 5) == 1:
#             scrolling = False
#         last_height = new_height


driver = webdriver.Chrome(ChromeDriverManager().install())
authorize(driver)
queries_text, messages_count = messages_count(driver)
stories_count = get_stories_count(driver)
# watch_stories(driver)
# scroll_recomendations(driver)
# scroll_feed(driver)
# scroll_explore(driver)

if queries_text is not None:
    print(queries_text)
else:
    print('Нет новых запросов на диалог')
print('Новых сообщений:', messages_count)

print('Новых историй:', stories_count)
