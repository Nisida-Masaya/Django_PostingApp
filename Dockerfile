FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/ 
#pipコマンドを最新にし、txtファイル内のパッケージ（後述）をpipインストール 
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install pillow 
COPY . /code/