# from flask import Flask, render_template, jsonify, request
# from pymongo import MongoClient
# import random
#
# app = Flask(__name__)
#
# client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
# db = client.dbsparta
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# @app.route('/showCat', methods=['GET'])
# def read_articles():
#     cats = list(db.cats.find({}, {'_id': False}))
#     cat = random.choice(cats)
#     return jsonify({'result': 'success', 'cat': cat})
#
# @app.route('/idolCat')
# def idolCat():
#     return render_template('idolCat.html')
#
# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)
#
#     # app > div > div:nth-child(3) > div:nth-child(3) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > figure > div > div._3A74U > div > div > a > div > img
import random

from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('idolCat.html')


@app.route('/idolCat', methods=['GET'])
def show_cat():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    cats = list(db.cats.find({}, {'_id': 0}))
    print("DB에서 cats 가져온 값:")
    print(cats)

    # Random 1개 선택
    # cat = random.choice(cats)

    # Random 2개 선택
    randomCats = random.sample(cats, 2)

    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'cats': randomCats})


@app.route('/random', methods=['GET'])
def random_cat():
    return render_template('random.html')

@app.route('/showCat', methods=['GET'])
def read_articles():
    cats = list(db.cats.find({}, {'_id': 0}))
    cat = random.choice(cats)

    return jsonify({'result': 'success', 'cat': cat})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
