# Django_PostingApp

## 参考記事
    https://qiita.com/bakupen/items/f23ce3d2325b4491a2dd
    https://book-reviews.blog/build-django-mysql-environment-with-docker-compose/
    https://prograshi.com/platform/docker/create-django-environment-on-docker/

# 環境構築作成手順

1 vscodeを新しいウィンドウで開く。

2 vscodeの上にマウスを持っていき、ターミナルの新しいターミナルを押す。

3 $ cd Desktop

4 Dockerfileを作成し以下を記述
 ---------------------------------------
  FROM python:3           
  ENV PYTHONUNBUFFERED 1  
  RUN mkdir /code          
  WORKDIR /code           
  COPY requirements.txt /code/ 
  #pipコマンドを最新にし、txtファイル内のパッケージ（後述）をpipインストール
  RUN pip install --upgrade pip && pip install -r requirements.txt && pip install pillow
  COPY . /code/            

 ---------------------------------------

5 Docker-compose.ymlを作成し以下を記述
 ---------------------------------------
  version: '3'
  services:
    db:
      image: mysql:5.7
      environment:
        MYSQL_ROOT_PASSWORD: root
        MYSQL_DATABASE: django-db
        MYSQL_USER: root
        MYSQL_PASSWORD: root
        TZ: 'Asia/Tokyo'
      command: mysqld --character-set-server=utf8 --collation-server=utf8_unicode_ci
    web:
      build: .
      command: python3 manage.py runserver 0.0.0.0:8000
      volumes:
        - .:/code
      ports:
        - "8000:8000"
      depends_on:
        - db

 ---------------------------------------

6 requirements.txtを作成し以下を記述
 ---------------------------------------
   Django
   Pillow #modelsでimageFieldを使うときに必要
   mysqlclient   # pythonでMySQLに接続するためのドライバ

 ---------------------------------------

7 docker compose up

8 docker compose run web django-admin startproject プロジェクト名 .

9 http://localhost:8000  にアクセスするとデフォルトページが表示される

10 docker compose run web python manage.py startapp アプリ名

11 