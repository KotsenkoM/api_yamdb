# api_yamdb
api_yamdb - это API для социальной сети, где пользователи могут поделиться впечатлением от увиденного, прослушанного или прочитанного, поставить свою оценку и узнать мнения других. 
***
### возможности:
* оставлять отзыв к произведению
* оценивать произведение в диапазоне от одного до десяти 
* смотреть рейтинг произведения
* авторизоваться по токену
*** 
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/iogin/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
***
Ссылка на локальный сервер:
http://127.0.0.1:8000/

Документация доступна по адресу:
http://127.0.0.1:8000/redoc/
***
###Пример работы API:

Запрос для добавление нового пользователя через подтверждение кода переданного на email:
```python
import requests
url = 'http://127.0.0.1:8000/api/v1/auth/signup/'
email = 'Тут ваш email'
username = 'Тут ваш username'
```
Ответ от API:
```json
{
  "email": "Тут ваш email", 
  "username": "Тут ваш username"
}
```
Подтверждение кода и получение token:
```python
import requests
url = 'http://127.0.0.1:8000/api/v1/auth/token/'
username = 'Тут ваш username'
confirmation_code = 'Тут ваш confirmation_code'
```
Ответ от API:
```json
{
  "token": "Тут ваш token"
