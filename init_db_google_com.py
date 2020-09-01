import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

def getCatImagePaths(catUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko)'}
    data = requests.get(catUrl, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    imageLinks = soup.select('img')
    urls = []
    for link in imageLinks:
        imgSrc = link['src']
        if "https" in imgSrc:
            print(imgSrc)
            urls.append(imgSrc)

    return urls


def insertImageUrl(imageUrl):
    doc = {
        'picture_path': imageUrl
    }

    db.cats.insert_one(doc)
    print('완료!', doc)


def insert_all():
    # db.cats.drop()
    catUrls = [
        'https://www.google.com/search?q=cat&tbm=isch&ved=2ahUKEwjvyYvb48XrAhUZO3AKHV65BbMQ2-cCegQIABAA&oq=cat&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQsQMyAggAMgUIABCxAzIFCAAQsQMyAggAMgIIADICCAAyAggAMgIIADoECAAQHjoECAAQAzoICAAQsQMQgwE6BwgjEOoCECdQ12VYmnNgl3VoAXAAeACAAbIBiAGJDJIBBDAuMTCYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=FxpNX6_iJZn2wAPe8paYCw&bih=821&biw=1440'
    ]

    for catUrl in catUrls:
        imagePaths = getCatImagePaths(catUrl)
        for path in imagePaths:
            insertImageUrl(path)

## 실행하기
insert_all()
