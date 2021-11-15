import requests
import sqlite3
import re
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pyshorteners
from sql import SQLighter
from os import system


#################Создание таблиц #########################################

bd=SQLighter('bd.db')
sql = sqlite3.connect('bd.db')
cursor = sql.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS post (text) """)
sql.commit()
cursor.execute(""" CREATE TABLE IF NOT EXISTS ac (token CHAR,ver INT, g CHAR,token_bot CHAR, chatid CHAR) """)
sql.commit()
cursor.execute(""" CREATE TABLE IF NOT EXISTS admitad (login CHAR, password CHAR) """)
sql.commit()
cursor.execute(""" CREATE TABLE IF NOT EXISTS grupp (grup CHAR) """)
sql.commit()
###########################################################################




def menu():
    print("[1]Инструкция")
    print("[2] Ввести данные")
    print("[3] Авторизоваться")
    print("[4] Запуск")

menu()
option = int(input("Введите номер команды:"))
while option != 0:
        if option == 1:
            print("Инструкция")
            system("read_me.docx")

        if option == 2:
            token = input("Введите токен vk: ")
            vers = input("Введите актуальную версию vk: ")
            group = input("Введите группу vk: ")
            count = 1
            offset = 1
            token_bot = input("Введите токен телеграм бота: ")
            chatID = input("Введите название чата: ")
            bd.add_ac(token, vers, group, token_bot, chatID)

        if option == 3:
            login = input("Введите логин: ")
            password = input("Введите Пароль: ")
            bd.add_av(login, password)

        if option==4:
            gruppa=input("Введите название группы:")
            bd.add_group(gruppa)

        if option==9:
            gruppa = input("Выберите группу: ")
            group = bd.group(gruppa)
            print(group)

        if option == 5:

            token = bd.token()
            vers = bd.vers()
            gruppa=input("Выберите группу: ")
            group = bd.group(gruppa)
            count = 1
            offset = 1

            for i in bd.token_bot():
                i
            token_bot = str(i)
            for j in bd.chat_id():
                j
            chatID = str(j)
            all_posts = []
            while offset < 1000:
                options = webdriver.ChromeOptions()

                # user-agent
                options.add_argument(
                    "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
                options.headless = True
                driver = webdriver.Chrome(
                    executable_path=r"G:\Alik\chromedriver.exe",
                    options=options)

                responce = requests.get('https://api.vk.com/method/wall.get',
                                        params={
                                            'access_token': token,
                                            'v': vers,
                                            'domain': group,
                                            'count': count,
                                            'offset': offset

                                        })

                data = responce.json()['response']['items']
                offset += 1
                all_posts.extend(data)
                time.sleep(1)
                for post in data:
                    try:
                        if post['attachments'][0]['type']:
                            img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                        else:
                            img_url = "pass"
                    except:
                        pass

                    try:

                        likes = post['likes']['count']
                        text = post['text']
                        text2 = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
                        url = re.search("(?P<url>https?://[^\s]+)", text).group("url")

                        print(text2, url)
                        if (not bd.text(text2)):
                            bd.add_text(text2)
                            headers = {
                                "Accept": "*/*",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
                            }
                            req = requests.get(url=url, headers=headers)
                            src = req.text
                            soup = BeautifulSoup(src, "lxml")
                            # Определяем количество страниц
                            original = soup.find("link", rel='canonical').get('href')
                            print(text2, original)

                            driver.get('https://store.admitad.com/ru/sign_in/')
                            time.sleep(0.5)
                            email_input = driver.find_element_by_id('id_login')
                            email_input.clear()
                            email_input.send_keys(bd.login())
                            time.sleep(0.5)
                            password_input = driver.find_element_by_id('id_password')
                            password_input.clear()
                            password_input.send_keys(bd.password())
                            time.sleep(0.5)
                            login_button = driver.find_element_by_id('id_sign_in').click()
                            time.sleep(0.5)

                            driver.get('https://store.admitad.com/ru/webmaster/deeplink_generator/')
                            time.sleep(0.5)

                            radio_button = driver.find_element_by_id('id_advcampaign_1').click()
                            time.sleep(0.5)
                            text_area = driver.find_element_by_id('id_list_of_links')
                            text_area.clear()
                            text_area.send_keys(original)
                            time.sleep(0.5)
                            genere_button = driver.find_element_by_id('gen_deeplinks_btn').click()
                            time.sleep(0.5)

                            src = driver.page_source
                            soup = BeautifulSoup(src, "lxml")
                            generated_links = soup.find("textarea", id='generated_links').text
                            print(generated_links)
                            # https://aliexpress.ru/item/1005001825910098.html
                            driver.get('https://bitly.com/')
                            time.sleep(0.5)
                            bitly_input = driver.find_element_by_id('shorten_url')
                            bitly_input.clear()
                            bitly_input.send_keys(generated_links)
                            time.sleep(0.5)
                            bitly_button = driver.find_element_by_id('shorten_btn').click()
                            time.sleep(5)
                            src = driver.page_source
                            soup = BeautifulSoup(src, "lxml")
                            short_link = soup.find("span", class_='short-link').find('a').get('href')

                            print("сокращенная ссылка",
                                  short_link)
                            img = requests.get(img_url)
                            with open("img.jpg", "wb") as f:
                                f.write(img.content)
                            img = open('img.jpg', 'rb')
                            # token_bot = '2084674142:AAGSL0dygxHw8dDCG_YRalu52aNMPUas4JQ'
                            # chatID = '@moi_ali_fy'
                            url = f'https://api.telegram.org/bot{token_bot}/sendPhoto?chat_id={chatID}'
                            data = {"caption": text2 + ' ' + short_link}

                            print(requests.post(url, data=data, files={"photo": img}))

                            time.sleep(1800)

                        else:
                            print("запись существует!!!")
                            pass


                    except Exception as ex:
                        print(ex)
                    finally:
                        driver.close()
                        driver.quit()



        print()
        menu()
        print()
        option = int(input("Введите номер команды:"))



def posts():

    token = 'c59aed4ec59aed4ec59aed4e17c5e3088acc59ac59aed4ea4e74c266f45f841b2947789'
    vers = 5.81
    group = 'krutie'
    count = 1
    offset = 1
    token_bot='2084674142:AAGSL0dygxHw8dDCG_YRalu52aNMPUas4JQ'
    chatID='moi_ali_fy'
    all_posts = []
    while offset < 1000:
        options = webdriver.ChromeOptions()

        # user-agent
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.headless=True
        driver = webdriver.Chrome(
            executable_path=r"G:\Alik\chromedriver.exe",
            options=options)

        responce = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': vers,
                                    'domain': group,
                                    'count': count,
                                    'offset': offset

                                })

        data = responce.json()['response']['items']
        offset += 1
        all_posts.extend(data)
        time.sleep(1)
        for post in data:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = "pass"
            except:
                pass


            try:

                likes = post['likes']['count']
                text = post['text']
                text2 = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
                url = re.search("(?P<url>https?://[^\s]+)", text).group("url")


                print(text2, url)
                if (not bd.text(text2)):
                    bd.add_text(text2)
                    headers = {
                        "Accept": "*/*",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
                    }
                    req = requests.get(url=url, headers=headers)
                    src = req.text
                    soup = BeautifulSoup(src, "lxml")
                    # Определяем количество страниц
                    original = soup.find("link", rel='canonical').get('href')
                    print(text2, original)

                    driver.get('https://store.admitad.com/ru/sign_in/')
                    time.sleep(0.5)
                    email_input = driver.find_element_by_id('id_login')
                    email_input.clear()
                    email_input.send_keys('scramas1')
                    time.sleep(0.5)
                    password_input = driver.find_element_by_id('id_password')
                    password_input.clear()
                    password_input.send_keys('gbUqfLg4c9kahZe')
                    time.sleep(0.5)
                    login_button = driver.find_element_by_id('id_sign_in').click()
                    time.sleep(0.5)

                    driver.get('https://store.admitad.com/ru/webmaster/deeplink_generator/')
                    time.sleep(0.5)

                    radio_button = driver.find_element_by_id('id_advcampaign_1').click()
                    time.sleep(0.5)
                    text_area = driver.find_element_by_id('id_list_of_links')
                    text_area.clear()
                    text_area.send_keys(original)
                    time.sleep(0.5)
                    genere_button = driver.find_element_by_id('gen_deeplinks_btn').click()
                    time.sleep(0.5)

                    src = driver.page_source
                    soup = BeautifulSoup(src, "lxml")
                    generated_links = soup.find("textarea", id='generated_links').text
                    print(generated_links)
                    # https://aliexpress.ru/item/1005001825910098.html
                    driver.get('https://bitly.com/')
                    time.sleep(0.5)
                    bitly_input = driver.find_element_by_id('shorten_url')
                    bitly_input.clear()
                    bitly_input.send_keys(generated_links)
                    time.sleep(0.5)
                    bitly_button = driver.find_element_by_id('shorten_btn').click()
                    time.sleep(5)
                    src = driver.page_source
                    soup = BeautifulSoup(src, "lxml")
                    short_link = soup.find("span", class_='short-link').find('a').get('href')

                    print("сокращенная ссылка",
                          short_link)
                    img=requests.get(img_url)
                    with open("img.jpg", "wb") as f:
                        f.write(img.content)
                    img = open('img.jpg', 'rb')
                    token_bot = '2084674142:AAGSL0dygxHw8dDCG_YRalu52aNMPUas4JQ'
                    chatID = '@moi_ali_fy'
                    url = f'https://api.telegram.org/bot{token_bot}/sendPhoto?chat_id={chatID}'
                    data = {"caption": text2+' '+short_link}





                    print(requests.post(url, data=data, files={"photo": img}))




                    time.sleep(1800)

                else:
                    print("запись существует!!!")
                    pass


            except Exception as ex:
                print(ex)
            finally:
                driver.close()
                driver.quit()









