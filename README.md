B1: Cài đặt virtualenv
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv venv -p python3.7

source venv/bin/activate

```

B2: Cài đặt môi trường cần thiết

```
pip install -r requirements.txt
```

B3: Chạy Rasa server

```
cd chat_nlu

rasa run --enable-api

```

B4: Chạy Web server

```
cd web_app
gunicorn --bind 0.0.0.0:5000 -w 4 app:app
```