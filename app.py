import random
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/', methods=['GET'])
# def show_cat():
#     # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
#     cats = list(db.cats.find({}, {'_id': 0}))
#     print("DB에서 cats 가져온 값:")
#     print(cats)
#
#     # Random 1개 선택
#     # cat = random.choice(cats)
#
#     # Random 2개 선택
#     randomCats = random.sample(cats, 2)
#
#     # 2. articles라는 키 값으로 article 정보 보내주기
#     return jsonify({'result': 'success', 'cats': randomCats})


@app.route('/idolCat')
def home():
    return render_template('idolCat.html')

@app.route('/')
@app.route('/random')
def random_cat():
    return render_template('random.html')

@app.route('/showCat', methods=['GET'])
def read_articles():
    cats = list(db.cats.find({}, {'_id': 0}))
    cat = random.choice(cats)

    return jsonify({'result': 'success', 'cat': cat})

@app.route('/addCat')
def add_cat():
    return render_template('addCat.html')

@app.route('/addCat', methods=['POST'])
def add_cat_image():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

    addCats = {
        'picture_path': path[1:]
    }
    # reviews에 review 저장하기
    db.cats.insert_one(addCats)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '냥님께서 잘 등록되셨습니다'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
