import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

def get_urls(catUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) https://unsplash.com/s/photos/kittenChrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(catUrl, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # app > div > div:nth-child(3) > div:nth-child(3) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > figure > div > div._3A74U > div > div > a > div > img
    # app > div > div:nth-child(3) > div:nth-child(3) > div > div:nth-child(1) > div > div > div:nth-child(2) > div:nth-child(1) > figure > div > div._3A74U > div > div > a > div > img
    # app > div > div:nth-child(3) > div:nth-child(3) > div > div:nth-child(1) > div > div > div:nth-child(2) > div:nth-child(2) > figure > div > div._3A74U > div > div > a > div > img
    # app > div > div:nth-child(4) > div:nth-child(3) > div > div._1w02r > div > div:nth-child(1) > figure > div > div._3A74U > a > div > img
    # app > div > div:nth-child(3) > div:nth-child(3) > div > div:nth-child(1) > div > div:nth-child(8) > figure > div > div._3A74U > a > div > img

    divs = soup.select('figure')

    urls = []
    for div in divs:
        img = div.select_one('img')
        if img is not None:
            imgSrc = img['src']
            if "profile" not in imgSrc:
                if "placeholder-avatars" not in imgSrc:
                    print(imgSrc)
                    if imgSrc not in urls:
                        urls.append(imgSrc)
    return urls

def insert_cats(url):
    doc = {
        'picture_path': url
    }

    db.cats.insert_one(doc)
    print('완료!', doc)


def insert_all():
    # db.cats.drop()
    catUrls = [
        'https://unsplash.com/s/photos/cat',
        'https://unsplash.com/s/photos/kitten',
        'https://unsplash.com/s/photos/cute-cat',
        'https://unsplash.com/s/photos/puppy'
    ]
    for catUrl in catUrls:
        urls = get_urls(catUrl)
        for url in urls:
            insert_cats(url)


## 실행하기
insert_all()
