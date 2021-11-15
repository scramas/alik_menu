

def post():
    token = 'c59aed4ec59aed4ec59aed4e17c5e3088acc59ac59aed4ea4e74c266f45f841b2947789'
    vers = 5.81
    group = 'doehalo'
    count = 100
    offset = 0
    all_posts = []
    while offset < 1000:
        responce = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': vers,
                                    'domain': group,
                                    'count': count,
                                    'offset': offset

                                })
        data = responce.json()['response']['items']
        offset += 100
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
                post1=cursor.execute('select * from post').fetchall()
                sql.commit()
                url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
                cursor.execute("insert into post (likes,body,url,url_img) values(?,?,?,?)",
                               (likes, text2, url, img_url,))
                sql.commit()




            except:
                pass

def link ():
    link=cursor.execute("select url from post").fetchall()
    sql.commit()
    listoutput = [i[0] for i in link]
    print(listoutput)
    j=0
    all_page={}

    with open(f"links.json", "w", encoding='utf8') as file:
            for i in listoutput:
                all_page[str(j)] = i
                j += 1

            json.dump(all_page, file, indent=4, ensure_ascii=False)
            file.close()
    with open(f"links.json", encoding='utf8') as file:
        all_pages = json.load(file)
        count=0
    for name_page, href_page in all_pages.items():
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
        }
        req = requests.get(url=href_page, headers=headers)
        src1 = req.text
        with open(f"pages/{count}_.html", "w", encoding='utf-8') as file:
            file.write(src1)

            count+=1

def canon():
    with open(f"links.json", encoding='utf8') as file:
        all_pages = json.load(file)
        # Перебераем страницы сайта и записываем и читаем
    for name_page, href_page in all_pages.items():
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
        }
        req = requests.get(url='http://alii.pub/629p2r', headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        # Определяем количество страниц
        original = soup.find("link", rel='canonical').get('href')
        print("1", original)
        time.sleep(3000)

def proveerka():
    with sql:
        return



    return print(test)
